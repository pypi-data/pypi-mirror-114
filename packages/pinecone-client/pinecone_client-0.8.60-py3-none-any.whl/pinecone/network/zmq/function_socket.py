from pinecone.network.zmq.socket_wrapper import SocketWrapper, Socket
from copy import deepcopy

from pinecone.utils.hash_ring import ConsistentHashRing
from pinecone.utils import load_numpy, dump_numpy, constants, replica_kube_hostname, replica_name
from pinecone.protos import core_pb2
from typing import List, Optional, Union, Dict
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import asyncio

import zmq


class FunctionSocket:
    """
    Given a socket with host == function_name, expose interface for connecting to shards and replicas of that function
    """

    def __init__(self, socket_spec: Socket, context: zmq.Context, native: bool, init_sockets: bool = True):
        """
        :param socket_spec:
        :param context:
        :param native:
        """
        self.socket_spec = socket_spec
        self.context = context
        self.native = native
        self.sockets = dict()  # type: Dict[str, SocketWrapper]
        self.sock = None
        self.executor = ThreadPoolExecutor()
        self.fn_name = socket_spec.host
        self.max_replica = 0

        if socket_spec.bind or self.fn_name is None:
            self.sock = SocketWrapper(socket_spec, context, native)
            self.hash_ring = None
        elif init_sockets:
            self.hash_ring = ConsistentHashRing.from_file(self.fn_name, native)
            self._init_sockets()

    def _init_sockets(self):
        if self.hash_ring:
            for shard in range(0, self.hash_ring.size):
                self.socket(shard=shard)
                self.socket(shard=shard, replica=0)
        else:
            self.socket()

    def socket_spec_for_host(self, host: str) -> Socket:
        new_spec = deepcopy(self.socket_spec)
        new_spec.host = host
        return new_spec

    def socket_for_host(self, host: str) -> SocketWrapper:
        if host not in self.sockets:
            new_spec = self.socket_spec_for_host(host)
            self.sockets[host] = SocketWrapper(new_spec, self.context, self.native,
                                               disable_loadbalance=host and '.' in host)
        return self.sockets[host]

    def get_host(self, shard: int = 0, replica: int = None) -> str:
        if self.native:
            return replica_name(self.fn_name, shard, replica)
        return replica_kube_hostname(self.fn_name, shard, replica)

    def socket(self, shard: int = 0, replica: int = None) -> SocketWrapper:
        return self.sock or self.socket_for_host(self.get_host(shard=shard, replica=replica))

    async def get_max_replica(self, shard: int):
        while await self.socket(shard, self.max_replica + 1).check_connection():
            self.max_replica += 1
        return self.max_replica

    async def refresh(self):
        while self.hash_ring:
            loop = asyncio.get_event_loop()
            new_hr = await loop.run_in_executor(self.executor, ConsistentHashRing.from_file, self.fn_name, self.native)
            if new_hr.size != self.hash_ring.size:
                logger.info(f'Hash ring size was: {self.hash_ring.size}. New size: {new_hr.size}')
                self.hash_ring = new_hr
            await asyncio.gather(*(sock.refresh_dns() for sock in self.all_socks))
            await asyncio.sleep(constants.KUBE_SYNC_TTL)

    def shard_msg(self, msg: 'core_pb2.Request') -> List[Optional['core_pb2.Request']]:
        return self.hash_ring.shard_msg(msg)

    async def send_msg(self, socket: SocketWrapper, msg: Union[bytes, core_pb2.Request]):
        if msg is None:
            return
        msg_bytes = msg if isinstance(msg, bytes) else msg.SerializeToString()
        await socket.send(msg_bytes)

    async def send(self, msg: core_pb2.Request):
        if self.sock:
            await self.send_msg(self.sock, msg)
        # next function is gateway or aggregator
        elif self.fn_name in [constants.GATEWAY_NAME, constants.AGGREGATOR_NAME]:
            sock = self.socket(shard=0, replica=msg.gateway_num)
            await self.send_msg(sock, msg)
        # next function is stateful
        elif self.hash_ring:
            if self.is_write_msg(msg):
                tasks = (self.send_msg(self.socket(s, replica=0), msg) for s, msg in enumerate(self.shard_msg(msg)))
                await asyncio.gather(*tasks)
            else:
                serialized_msg = msg.SerializeToString()
                tasks = (self.send_msg(self.socket(shard), serialized_msg) for shard in range(0, self.hash_ring.size))
                await asyncio.gather(*tasks)
        # next function is other, e.g. transformer
        else:
            await self.send_msg(self.socket(), msg)

    async def send_raw(self, msg: bytes, shard: int = None, replica: int = None):
        await self.send_msg(self.socket(shard, replica), msg)

    def is_write_msg(self, msg: core_pb2.Request) -> bool:
        req_type = msg.WhichOneof('body')
        return req_type not in ['info', 'query', 'fetch']

    async def recv(self) -> bytes:
        return await self.socket().recv()

    def close(self):
        if self.sock:
            self.sock.close()
        else:
            for sock in self.sockets.values():
                sock.close()

    @property
    def all_socks(self) -> List[SocketWrapper]:
        if self.sock:
            return [self.sock]
        return list(self.sockets.values())
