from pinecone.protos import core_pb2
from pinecone.utils import constants
from pinecone.utils import get_hostname, tracing
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket
from pinecone.network.zmq.function_socket import SocketWrapper, FunctionSocket

from loguru import logger
from typing import List, Dict
import asyncio
import zmq
import zmq.asyncio

from ddtrace import tracer
from ddtrace.tracer import Context


class ZMQServlet:

    def __init__(self, servlet_spec: ServletSpec):
        self.spec = servlet_spec
        self.context = zmq.asyncio.Context()

        self.exception = None
        if len(self.spec.in_sockets) > 0:
            self.zmq_ins = [self.init_socket(in_sock) for in_sock in self.spec.in_sockets]  # type: List[FunctionSocket]
        self.zmq_outs = {r: [self.init_socket(s) for s in sockets]
                         for r, sockets in self.spec.out_sockets.items()}  # type: Dict[str, List[FunctionSocket]]

        self.gateway_control_sock = self.init_socket(Socket(False, SocketType.PUSH, constants.ZMQ_CONTROL_PORT,
                                                            host=constants.GATEWAY_NAME))

        self.msg_sent = 0
        self.msg_recv = 0

        self.running_handlers = 0
        self.handlers_done = asyncio.Event()

    @property
    def pretty_name(self) -> str:
        return self.spec.function_name + " shard:" + str(self.spec.shard) + " replica:" + str(self.spec.replica)

    def handle_exception(self, loop: asyncio.AbstractEventLoop, context):
        # context["message"] will always be there; but context["exception"] may not
        if "exception" in context:
            self.exception = context['exception']
        msg = context.get("exception", context["message"])
        logger.info(f"Shutting down...Caught exception: {msg}")
        loop.stop()
        self.cleanup()

    async def wait_handlers_done(self):
        while self.running_handlers > 0:
            self.handlers_done.clear()
            await self.handlers_done.wait()

    async def handle_msg(self, msg: core_pb2.Request):
        route = core_pb2.Route(function=get_hostname(), function_id=self.spec.shard)
        route.start_time.GetCurrentTime()

        msg_context = Context(trace_id=msg.telemetry_trace_id, span_id=msg.telemetry_parent_id)
        tracer.context_provider.activate(msg_context)
        with tracer.trace(self.spec.function_name) as span:
            tracing.set_span_tags(span, msg)
            msg.telemetry_parent_id = span.span_id
            if self.spec.handle_msg:
                self.running_handlers += 1
                response = await self.spec.handle_msg(msg)
                self.running_handlers -= 1
                self.handlers_done.set()
                route.end_time.GetCurrentTime()
                msg.routes.append(route)
                if response:
                    if self.spec.shard != 0:
                        response.shard_num = self.spec.shard
                    await self.send_msg(response)
                    del response
        del msg

    async def poll_sock(self, sock: SocketWrapper):
        loop = asyncio.get_event_loop()
        while True:
            msg = await self.recv_msg(sock)
            loop.create_task(self.handle_msg(msg))

    def start_polling(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [loop.create_task(self.poll_sock(sock.socket())) for sock in self.zmq_ins]

    def start_reload_task(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [loop.create_task(sock_fn.refresh()) for sock_fn in self.all_socks]

    async def send_msg(self, msg: 'core_pb2.Request'):
        self.msg_sent += 1
        send_sockets = []
        for path in {msg.path, '*'}:
            send_sockets.extend(self.zmq_outs.get(path, []))

        for fn_sock in send_sockets:
            await fn_sock.send(msg)

        if len(send_sockets) == 0 and msg.path != 'none':
            logger.warning('{}: no out socket_spec for path {}'.format(get_hostname(), msg.path))

        if msg.traceroute:
            receipt = core_pb2.TraceRoute(request_id=msg.request_id, client_id=msg.client_id,
                                          client_offset=msg.client_offset, routes=msg.routes)
            await self.gateway_control_sock.send_raw(receipt.SerializeToString(), replica=msg.gateway_num)

    async def recv_msg(self, sock: SocketWrapper) -> 'core_pb2.Request':
        msg = await sock.recv()
        msg_pb = core_pb2.Request()
        msg_pb.ParseFromString(msg)
        self.msg_recv += 1
        return msg_pb

    def init_socket(self, socket: Socket) -> FunctionSocket:
        if socket.bind:
            logger.info(f"{get_hostname()}:  Listening on {socket.host}:{socket.port}")
        else:
            logger.info(f"{get_hostname()}: Connecting to {socket.host}:{socket.port}")
        return FunctionSocket(socket, self.context, self.spec.native)

    @property
    def all_socks(self) -> List[FunctionSocket]:
        return [*self.zmq_ins, *[sock for sock_list in self.zmq_outs.values() for sock in sock_list]]

    def cleanup(self):
        for sock in self.all_socks:
            sock.close()
