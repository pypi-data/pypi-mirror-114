#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#
from pinecone.network.zmq.function_socket import FunctionSocket
from pinecone.utils.hash_ring import ConsistentHashRing

from .exceptions import InvalidOffsetException, IndexBusyException
from pinecone.protos import core_pb2
from pinecone.network.zmq.servlet import ZMQServlet
from pinecone.utils import open_or_create, get_hostname, wal, get_current_namespace, index_state, format_error_msg
from pinecone.utils.exceptions import RestartException
from pinecone.utils.constants import ZMQ_LOG_PORT, KUBE_SYNC_TTL, ZMQ_PORT_IN, IndexState, COMPACT_WAL_THRESHOLD
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket
from pinecone.network.zmq.socket_wrapper import SocketWrapper

from typing import Iterable, Tuple, List, Union
from loguru import logger

import concurrent.futures
from threading import Lock
import asyncio
import os
import functools
import requests


class WALServlet(ZMQServlet):
    """
    ZMQServlet for distributed stateful functions to provide
    - client ordering guarantees
    - replay recovery from disk
    - leader-follower replication
    """

    def __init__(self, servlet_spec: ServletSpec, path: str, volume_request: int = 15):
        super().__init__(servlet_spec)
        self.replica = servlet_spec.replica
        self.wal_size_limit = volume_request * (10 ** 9) * COMPACT_WAL_THRESHOLD  # translate to GB

        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.log_in = self.init_socket(self.log_in_socket)
        self.log_out = self.init_socket(self.log_out_socket)

        os.makedirs(path, exist_ok=True)

        self.log_path = os.path.join(path, 'log')
        self.tmp_log_path = os.path.join(path, 'tmp_log')  # for compaction
        self.log_file = open_or_create(self.log_path)
        self.log_lock = Lock()

        self.log_compaction_started = False

        self.last = core_pb2.Request()
        self.size = self.load_size()

        self.acked_offset = 0  # wal offset acked

        self.hash_ring = ConsistentHashRing.from_file(servlet_spec.function_name, servlet_spec.native)
        self.rebalance_requested = False
        self.rebalance_failed = False

        self._rebalance_sock_spec = Socket(False, SocketType.PUSH, ZMQ_PORT_IN, self.spec.function_name)
        self.rebalance_sock = FunctionSocket(self._rebalance_sock_spec, self.context, self.spec.native)

        self.index_ready = asyncio.Event()
        self.index_ready.set()

        self.compact_log_done = asyncio.Event()
        self.loading_from_wal = True

    @property
    def log_in_socket(self):
        return Socket(True, SocketType.PULL, ZMQ_LOG_PORT, host=get_hostname())

    @property
    def log_out_socket(self):
        return Socket(False, SocketType.PUSH, host=self.spec.function_name, port=ZMQ_LOG_PORT)

    def load_size(self):
        size = 0
        for pos, entry in self.sync_replay_log(0):
            size += 1
            self.last = entry
        return size

    def cleanup(self):
        self.log_file.close()
        super().cleanup()

    @property
    def leader(self):
        return self.replica == 0

    async def poll_log_socks(self):
        while True:
            msg = await self.recv_log_msg()
            await self.handle_log_msg(msg)

    def trigger_rebalance_shards(self):
        try:
            url = os.environ.get('CONTROLLER_URL')
            logger.info(f"{get_hostname()}: Triggering rebalance to {url}")

            project_name = get_current_namespace().replace(f"{self.spec.service_name}-", "")
            if len(project_name) == "":
                headers = {}
            else:
                # user label and user_name are placeholders, not used
                x_user_id = ".".join(['user_label', 'user_name', project_name])
                headers = {'x-user-id': x_user_id}
            resp = requests.patch(f'{url}/services/{self.spec.service_name}',
                                  json={'function': {'name': self.spec.function_name, 'shards': self.hash_ring.size + 1}},
                                  headers=headers).json()
            logger.info(resp)
            if not resp['success']:
                logger.error(f"Failed to trigger rebalance: {resp['msg']}. project: {project_name}. "
                             f"service: {self.spec.service_name}. function: {self.spec.function_name}. headers: {headers}")
                self.rebalance_failed = True
        except Exception as e:
            logger.error(e)
            self.rebalance_failed = True

    async def index_busy(self, msg: core_pb2.Request):
        format_error_msg(msg, IndexBusyException("Index busy reloading, try again in a minute."),
                         self.spec.function_name)
        await self.send_msg(msg)

    async def poll_sock(self, sock: SocketWrapper):
        loop = asyncio.get_event_loop()
        while True:
            msg = await self.recv_msg(sock)
            if self.loading_from_wal:
                await asyncio.sleep(msg.timeout * 0.75)
                if self.loading_from_wal:
                    await self.index_busy(msg)
                    continue

            if self.hash_ring:
                msg.num_shards = self.hash_ring.size

            if self.use_wal(msg):
                await self.handle_msg_wal(msg)
            else:
                loop.create_task(self.handle_msg(msg))

    async def kube_sync_task(self):
        """
        Dynamically relaods number of shards and number of replicas from the control plane
        :return:
        """
        loop = asyncio.get_event_loop()
        while True:
            new_hr = await loop.run_in_executor(self.executor, ConsistentHashRing.from_file, self.spec.function_name,
                                                self.spec.native)
            if self.hash_ring and new_hr.size != self.hash_ring.size:
                logger.info(f'Function size was: {self.hash_ring.size}. New size: {new_hr.size}. Rebalancing.')
                self.hash_ring = new_hr

                await self.start_compact_log(rebalance=True)
                self.rebalance_requested = False
            await self.check_for_new_replicas()
            await asyncio.sleep(KUBE_SYNC_TTL)

    def start_reload_task(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [*super().start_reload_task(), loop.create_task(self.kube_sync_task())]

    def start_polling(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [*(loop.create_task(self.poll_sock(sock.socket())) for sock in self.zmq_ins), loop.create_task(self.poll_log_socks())]

    def use_wal(self, msg: core_pb2.Request) -> bool:
        req_type = msg.WhichOneof('body')
        return req_type in ['index', 'delete']

    async def handle_write(self, msg: core_pb2.Request):
        self.index_ready.clear()
        await self.wait_handlers_done()
        await self.handle_msg(msg)
        self.index_ready.set()

    async def handle_msg_wal(self, msg: core_pb2.Request):
        """
        Leader handles write messages. Checks that they won't fill up index, optionally triggers rebalance,
        and then acknowledges them / sends to replicas
        :param msg:
        :return:
        """
        msg_type = msg.WhichOneof('body')
        if self.hash_ring and msg_type == 'index':
            shard_msg = self.hash_ring.shard_msg(msg)
            for shard, msg in enumerate(shard_msg):
                if shard != self.spec.shard and len(msg.index.ids) > 0:
                    await self.forward_shard_msg(msg, shard)
            msg = shard_msg[self.spec.shard]
        elif self.rebalance_requested:
            format_error_msg(msg, IndexBusyException("Index rebalancing, try again shortly"), self.spec.function_name)
            await self.send_msg(msg)

        new_offset = await self.put(msg)

        idx_state = await self.run_sync(index_state)
        if msg_type == 'index':
            if idx_state == IndexState.FULL:
                rb_msg = "Rebalancing shards, try again in a minute." if self.rebalance_requested else ""
                if self.rebalance_failed:
                    rb_msg = "Scaling up shards failed. Make sure your client is up to date!"
                format_error_msg(msg, RuntimeError(f"Index full, cannot accept upserts. {rb_msg}"), self.pretty_name)
                await self.send_msg(msg)
                return
            elif idx_state == IndexState.PENDING and not self.rebalance_requested:
                await self.run_sync(self.trigger_rebalance_shards)
                self.rebalance_requested = True

        await self.handle_write(msg)
        await self.ack(new_offset)

    async def start_replay_to_replica(self, replica: int, offset: int):
        event_loop = asyncio.get_event_loop()
        await self.run_sync(self.handle_replay_request, event_loop, replica, offset, end_offset=self.acked_offset)

    async def handle_log_msg(self, msg: 'core_pb2.LogEntry'):
        """
        Handles replay messages from replicas to leader, and log entries being sent from leader to replicas
        :param msg:
        :return:
        """
        if not self.leader:
            try:
                if await self.put(msg.entry, offset=msg.offset):
                    await self.handle_write(msg.entry)
                    await self.ack(offset=msg.offset)
            except InvalidOffsetException:
                logger.warning(f"Received invalid offset {msg.offset}")
                await self.send_log_msg(self.get_replay_request(), self.acked_offset)
        elif msg.ack.replay:
            await self.start_replay_to_replica(msg.ack.replica, msg.offset)
        del msg

    async def recv_log_msg(self):
        msg = await self.log_in.socket().recv()
        msg_pb = core_pb2.LogEntry()
        msg_pb.ParseFromString(msg)
        return msg_pb

    async def send_log_msg(self, msg: Union['core_pb2.LogEntry', bytes], replica: int):
        data = msg if type(msg) == bytes else msg.SerializeToString()
        await self.log_out.send_raw(data, shard=self.spec.shard, replica=replica)

    async def run_sync(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, functools.partial(func, *args, **kwargs))

    def sync_put(self, entry: core_pb2.Request, offset: int):
        if (not offset) or (self.size + 1) == offset:
            with self.log_lock:
                wal.write_log_entry(self.log_file, entry)
                self.size += 1
                # we need to copy the message, because it might get changed later on
                self.last.CopyFrom(entry)
                logfile_size = self.log_file.tell()
            return logfile_size, self.size

        # ignore because the msg has already been added
        elif offset <= self.size:
            return self.log_file.tell(), None
        else:
            raise InvalidOffsetException

    async def put(self, item: core_pb2.Request, offset: int = None):
        if not self.leader and offset is None:
            raise RuntimeError(f"{get_hostname()} Attempted to write directly to replica {self.replica} instead of leader")
        logfile_size, offset = await self.run_sync(self.sync_put, item, offset)
        if logfile_size > self.wal_size_limit and not self.log_compaction_started:
            loop = asyncio.get_event_loop()
            logger.info(f'Starting WAL compaction. Log size: {logfile_size}')
            loop.create_task(self.start_compact_log())
        return offset

    async def check_for_new_replicas(self):
        old_max_replica = self.log_out.max_replica
        max_replica = await self.log_out.get_max_replica(self.spec.shard)
        logger.success(f"Max replica: {max_replica} old: {old_max_replica}")

        msg = core_pb2.LogEntry(entry=self.last, offset=self.acked_offset)
        serialized_msg = msg.SerializeToString()
        for replica in range(old_max_replica + 1, max_replica + 1):
            logger.info(f"New replica {replica} detected, replaying WAL")
            await self.send_log_msg(serialized_msg, replica)

    def sync_replay_log(self, offset: int, end_offset: int = None) -> Iterable[Tuple[int, core_pb2.Request]]:
        """
        Replay log from offset 0 (inclusive) to end_offset (exclusive)
        :param offset:
        :param end_offset:
        :return:
        """
        with open_or_create(self.log_path) as log_file:
            log_file.seek(0)
            pos = 0
            while True:
                entry, msg_size = wal.read_entry(log_file)

                if msg_size == 0 or (end_offset and pos >= end_offset):
                    break
                if pos >= offset:
                    yield pos, entry
                pos += 1

    async def forward_shard_msg(self, msg: core_pb2.Request, shard: int):
        await self.rebalance_sock.send_msg(self.rebalance_sock.socket(shard, replica=0), msg)

    def handle_replay_request(self, loop: asyncio.AbstractEventLoop, replica: int, offset: int, end_offset: int = None):
        logger.info(f"Replaying log from offset {offset} to replica {replica}")
        for pos, entry in self.sync_replay_log(offset, end_offset=end_offset):
            asyncio.run_coroutine_threadsafe(self.send_log_msg(core_pb2.LogEntry(entry=entry,
                                                                                 offset=pos), replica), loop)

    async def ack(self, offset: int):
        if self.acked_offset > offset:
            logger.warning('Acked offset less than current offset')
        elif self.acked_offset + 1 > offset:
            logger.warning('Acked by more than one offset')

        self.acked_offset = offset
        if self.leader:
            msg = core_pb2.LogEntry(entry=self.last, offset=offset)
            serialized_msg = msg.SerializeToString()

            for r in range(1, self.log_out.max_replica + 1):
                await self.send_log_msg(serialized_msg, r)

    def get_replay_request(self,):
        ack = core_pb2.Ack(replica=self.replica, replay=True)
        logger.info(f"Sending replay request for offset {self.acked_offset}")
        return core_pb2.LogEntry(offset=self.acked_offset, ack=ack)

    def load_sync(self, handler):
        logger.info(f'Recovering from local WAL: offset: {self.acked_offset}')
        self.loading_from_wal = True
        for offset, entry in self.sync_replay_log(self.acked_offset):
            try:
                handler(entry)
            except Exception as e:  # ignore messages that fail
                logger.info(f'Error handling msg while recovering from WAL. offset: {offset} error: {e}')
            self.acked_offset = offset
        self.loading_from_wal = False

    def swap_log_files(self, end_file_offset: int):
        tmp_log_file = open(self.tmp_log_path, "r+b")

        with open_or_create(self.log_path) as log_file:
            log_file.seek(end_file_offset)
            while True:
                entry, msg_size = wal.read_entry(log_file)
                if msg_size == 0:
                    break
                wal.write_log_entry(tmp_log_file, entry)

        tmp_log_file.close()
        self.log_file.close()
        os.remove(self.log_path)
        os.rename(self.tmp_log_path, self.log_path)
        self.log_file = open(self.log_path, "r+b")

    async def start_compact_log(self, rebalance=False):
        while self.log_compaction_started:
            logger.info('Waiting for log compaction to be done to start again...')
            await self.compact_log_done.wait()
            self.compact_log_done.clear()

        with self.log_lock:
            self.log_compaction_started = True
            end_file_offset = self.log_file.tell()
            self.log_file.flush()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(concurrent.futures.ProcessPoolExecutor(), wal.compact_log,
                                   self.log_path, self.tmp_log_path, end_file_offset, self.hash_ring, self.spec.shard,
                                   self._rebalance_sock_spec if self.leader else None, self.spec.native)

        logger.info("Starting swap log files...")
        await self.run_sync(self.swap_log_files, end_file_offset)
        logger.info("Finishined swapping log files.")
        self.log_compaction_started = False
        self.compact_log_done.set()
        if rebalance:
            raise RestartException

    @property
    def all_socks(self):
        return [*super().all_socks, self.log_in, self.log_out]
