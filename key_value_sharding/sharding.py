
NUM_SHARDS = 3  # The number of shards (databases)

def get_shard(key):
    hash_key = hash(key)
    return hash(key) % NUM_SHARDS