#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.protos import core_pb2

import zmq
import zmq.asyncio
import enum
from typing import Callable, Awaitable, Optional, Dict, List
import os


class SocketType(enum.Enum):
    PUB = 1
    SUB = 2
    PAIR = 3
    PULL = 4
    PUSH = 5

    @classmethod
    def proxy_pair(cls, socket_type):
        return {
            cls.PUSH: cls.PULL,
            cls.PULL: cls.PUSH
        }[socket_type]


class Socket(object):

    def __init__(self,
                 bind: bool,
                 sock_type: SocketType,
                 port: int = None,
                 host: str = None):
        self.host = host
        self.port = port
        self.sock_type = sock_type
        self.bind = bind

    def get_conn_string(self, native: bool) -> str:
        sock_path = '/tmp/'
        if self.bind:
            if native:
                ipc_sock = os.path.join(sock_path, self.host) + str(self.port)

                if os.path.exists(ipc_sock):
                    os.remove(ipc_sock)

                conn_str = "ipc://{}".format(ipc_sock)
            else:
                conn_str = "tcp://*:{}".format(self.port)
        else:
            if native:
                ipc_sock = os.path.join(
                    sock_path, self.host) + str(self.port)
                conn_str = 'ipc://{}'.format(ipc_sock)
            else:
                conn_str = 'tcp://{}:{}'.format(self.host, self.port)
        return conn_str

    def zmq(self, context: 'zmq.context') -> 'zmq.Socket':
        assert (self.port and self.bind) or self.host
        return context.socket({
                                  SocketType.PUB: lambda: zmq.PUB,
                                  SocketType.SUB: lambda: zmq.SUB,
                                  SocketType.PAIR: lambda: zmq.PAIR,
                                  SocketType.PULL: lambda: zmq.PULL,
                                  SocketType.PUSH: lambda: zmq.PUSH
                              }[self.sock_type]())


class ServletSpec:

    def __init__(self, handle_msg: Optional[Callable[['core_pb2.Request'], Awaitable['core_pb2.Request']]],
                 in_sockets: List[Socket],
                 out_sockets: Dict[str, List[Socket]],
                 native: bool = True,
                 function_name: str = 'no_function',
                 shard: int = 0,
                 replica: Optional[int] = 0,
                 get_stats: Callable = dict,
                 service_name: str = None):
        """
                :param handle_msg:
                :param in_sockets:
                :param out_sockets:
                :param native:
                :param function_name:
                :param replica:
                :param get_stats:
                :param service_name:
        """
        self.in_sockets = in_sockets
        self.out_sockets = out_sockets
        self.native = native  # run natively in python with IPC networking
        self.handle_msg = handle_msg
        self.function_name = function_name
        self.replica = replica
        self.get_stats = get_stats
        self.service_name = service_name
        self.shard = shard
