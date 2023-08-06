from pinecone.utils.hash_ring import ConsistentHashRing
import pickle


def test_hash_ring():
    h = ConsistentHashRing(shards=4)
    pickle_str = h.to_string()
    # print(pickle_str)
    print(len(pickle_str))
    _h = ConsistentHashRing.from_string(pickle_str)
    assert _h.size == 4


if __name__ == "__main__":
    test_hash_ring()
