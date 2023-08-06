from __future__ import annotations

from typing import Optional, List

from pinecone.protos import core_pb2
from pinecone.utils import constants, load_numpy, dump_numpy

import bisect
from hashlib import md5
import pickle
import os


class ConsistentHashRing:

    def __init__(self, shards=1, partitions=100):
        self.partitions = partitions
        self._keys = []
        self._nodes = {}
        self._size = 0

        for i in range(shards):
            self.add_node(str(i))

    def resize(self, new_size: int):
        assert new_size >= self.size
        for i in range(self.size, new_size):
            self.add_node(str(i))

    @property
    def size(self):
        return self._size

    def _hash(self, key: str):
        return int(md5(key.encode('utf-8')).hexdigest(), 16)

    def _repl_iterator(self, nodename: str):
        return (self._hash(f"{nodename}:{i}") for i in range(self.partitions))

    def add_node(self, node: str):
        for hash_ in self._repl_iterator(node):
            if hash_ in self._nodes:
                raise ValueError(f"Node name {node} already exists")
            self._nodes[hash_] = node
            bisect.insort(self._keys, hash_)
        self._size = int(len(self._keys) / self.partitions)

    def __delitem__(self, nodename: str):
        for hash_ in self._repl_iterator(nodename):
            del self._nodes[hash_]
            index = bisect.bisect_left(self._keys, hash_)
            del self._keys[index]

    def __getitem__(self, key: str):
        hash_ = self._hash(key)
        start = bisect.bisect(self._keys, hash_) % len(self._keys)
        return self._nodes[self._keys[start]]

    def to_string(self):
        return pickle.dumps(self, protocol=0).decode(encoding='ascii')

    @classmethod
    def from_string(cls, pkl_str: str):
        return pickle.loads(pkl_str.encode(encoding='ascii'))

    @classmethod
    def from_file(cls, fn_name: str, native: bool) -> Optional[ConsistentHashRing]:
        hash_path = constants.NATIVE_SHARD_PATH if native else constants.SHARD_CONFIG_PATH
        hash_ring_path = os.path.join(hash_path, fn_name)
        if not os.path.exists(hash_ring_path):
            return None
        with open(hash_ring_path, 'r') as hr_file:
            return ConsistentHashRing.from_string(hr_file.read())

    def shard_msg(self, msg: 'core_pb2.Request') -> List[Optional['core_pb2.Request']]:
        req_type = msg.WhichOneof('body')
        num_shards = self.size
        req = getattr(msg, req_type)
        msg_shards = [int(self[id_]) for id_ in req.ids]

        shard_msgs = [core_pb2.Request() for i in range(num_shards)]
        data = load_numpy(req.data) if req_type == 'index' else None
        for shard_id, new_msg in enumerate(shard_msgs):
            new_msg.CopyFrom(msg)
            relevant_indices = [i for i in range(len(msg_shards)) if msg_shards[i] == shard_id]
            new_req = getattr(new_msg, req_type)
            relevant_ids = [new_req.ids[i] for i in relevant_indices]
            del new_req.ids[:]
            new_req.ids.extend(relevant_ids)
            if data is not None and len(data) > 0:
                new_req.data.CopyFrom(dump_numpy(data[relevant_indices, :]))
        return shard_msgs
