# sharding.py

NUM_SHARDS = 3

def get_shard():
    yield from range(NUM_SHARDS)
