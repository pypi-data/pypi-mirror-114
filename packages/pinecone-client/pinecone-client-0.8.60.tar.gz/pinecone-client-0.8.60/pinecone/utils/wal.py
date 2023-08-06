from typing import BinaryIO
import google.protobuf.message
from pinecone.protos import core_pb2
from pinecone.utils.hash_ring import ConsistentHashRing
from pinecone.utils import constants
from pinecone.network.zmq.function_socket import Socket, FunctionSocket

from loguru import logger
import os
from . import load_numpy, dump_numpy
from collections import defaultdict
import zmq

OFFSET_BYTES = 8
SIZE_BYTES = 4
BYTEORDER = 'big'


def read_size(log_file: BinaryIO):
    return int.from_bytes(log_file.read(SIZE_BYTES), BYTEORDER)


def read_proto(log_file: BinaryIO, size: int):
    msg_bytes = log_file.read(size)
    entry = core_pb2.Request()
    try:
        entry.ParseFromString(msg_bytes)
    except google.protobuf.message.DecodeError:
        logger.error(f"failed to load msg from WAL: {msg_bytes}")
    return entry, len(msg_bytes)


def read_entry(log_file: BinaryIO):
    size = read_size(log_file)
    entry, msg_size = read_proto(log_file, size)
    read_size(log_file)
    return entry, msg_size


def read_entry_backwards(log_file: BinaryIO) -> [core_pb2.Request, int]:
    if log_file.tell() == 0:
        return core_pb2.Request(), 0
    log_file.seek(-SIZE_BYTES, os.SEEK_CUR)
    size = read_size(log_file)
    log_file.seek(-(SIZE_BYTES + size), os.SEEK_CUR)
    entry, msg_size = read_proto(log_file, size)
    log_file.seek(-(SIZE_BYTES + size), os.SEEK_CUR)  # reset to end of previous entry
    return entry, msg_size


def write_log_entry(log_file: BinaryIO, entry: core_pb2.Request):
    log_file.seek(0, os.SEEK_END)
    entry_bytes = entry.SerializeToString()
    size = len(entry_bytes).to_bytes(SIZE_BYTES, BYTEORDER)
    log_file.write(size + entry_bytes + size)
    log_file.flush()


def get_sync_sock(context: zmq.Context, fn_sock: FunctionSocket, open_sockets: dict, host: str, native: bool):
    if host not in open_sockets:
        sock_spec = fn_sock.socket_spec_for_host(host)
        sock = sock_spec.zmq(context)
        sock.set_hwm(100)  # needs to be set before bind/connect
        sock.setsockopt(zmq.RCVBUF, 2 * constants.MAX_MSG_SIZE)
        sock.setsockopt(zmq.SNDBUF, 2 * constants.MAX_MSG_SIZE)

        conn_str = sock_spec.get_conn_string(native)
        sock.connect(conn_str)
        open_sockets[host] = sock
    return open_sockets[host]


def compact_log(log_path: str, tmp_log_path: str, end_file_offset: int, hash_ring: ConsistentHashRing = None,
                cur_shard: int = None, rebalance_sock_spec: Socket = None, native: bool = None):
    open_sockets = dict()
    if rebalance_sock_spec:
        context = zmq.Context()
        fn_sock = FunctionSocket(rebalance_sock_spec, context, native, init_sockets=False)
    else:
        context = None
        fn_sock = None

    with open(log_path, 'rb') as log_file:
        with open(tmp_log_path, 'w+b') as tmp_log_file:
            log_file.seek(end_file_offset)
            ids_seen = defaultdict(set)
            while True:
                entry, msg_size = read_entry_backwards(log_file)
                if msg_size == 0:
                    break

                new_entry = core_pb2.Request()
                if entry.WhichOneof('body') == 'index':
                    keep_idx = []
                    for i, item_id in enumerate(entry.index.ids):
                        if item_id not in ids_seen[entry.namespace]:
                            new_entry.index.ids.append(item_id)
                            keep_idx.append(i)
                            ids_seen[entry.namespace].add(item_id)

                    data = load_numpy(entry.index.data)
                    new_entry.index.data.CopyFrom(dump_numpy(data[keep_idx, :]))
                    size = len(new_entry.index.ids)
                else:  # delete
                    for item_id in entry.delete.ids:
                        if item_id not in ids_seen[entry.namespace]:
                            new_entry.delete.ids.append(item_id)
                            ids_seen[entry.namespace].add(item_id)
                    size = len(new_entry.delete.ids)
                if size > 0:  # only write the request if it has data in it
                    if hash_ring:
                        shard_msg = hash_ring.shard_msg(new_entry)
                        for shard, msg in enumerate(shard_msg):
                            if shard != cur_shard and len(msg.index.ids) > 0 and fn_sock:
                                msg.client_offset = 0
                                msg.path = 'none'
                                remote_host = fn_sock.get_host(shard, replica=0)
                                forward_sock = get_sync_sock(context, fn_sock, open_sockets, remote_host, native)
                                forward_sock.send(msg.SerializeToString())

                        new_entry = shard_msg[cur_shard]
                    write_log_entry(tmp_log_file, new_entry)
