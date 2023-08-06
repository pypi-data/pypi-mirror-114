#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.utils.tracing import init_tracer, init_profiler
from pinecone.utils import exceptions, get_hostname
init_tracer()
init_profiler()

import argparse
from loguru import logger
from pinecone.network.zmq_service import ZMQService

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Load functions with config')

    ZMQService.add_args(parser)

    args, unk = parser.parse_known_args()

    while True:
        ZMQService.start_with_args(args)
        logger.success(f"Exited {get_hostname()}")
