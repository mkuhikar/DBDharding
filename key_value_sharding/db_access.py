# db_access.py

import psycopg2
from sharding import get_shard, NUM_SHARDS

# Connection details for each shard (update with your database credentials)
shard_configs = {
    0: {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'qazwsx',
        'database': 'shard_0'
    },
    1: {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'qazwsx',
        'database': 'shard_1'
    },
    2: {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'qazwsx',
        'database': 'shard_2'
    },
}

def get_connection(key):
    shard_id = get_shard(key)
    config = shard_configs[shard_id]
    return psycopg2.connect(**config)

def store_data(key, value):
    conn = get_connection(key)
    cursor = conn.cursor()
    query = "INSERT INTO data (key, value) VALUES (%s, %s)"
    cursor.execute(query, (key, value))
    conn.commit()
    cursor.close()
    conn.close()

def get_data(key):
    conn = get_connection(key)
    cursor = conn.cursor()
    query = "SELECT value FROM data WHERE key = %s"
    cursor.execute(query, (key,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def create_data_table():
    # Loop through all the shards and create the 'data' table in each of them
    for shard_id in range(NUM_SHARDS):
        config = shard_configs[shard_id]

        try:
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()

            # Create the 'data' table if it does not exist
            query = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_files VARCHAR(255) PRIMARY KEY,
                file_data_chunk BYTEA
            )
            """
            cursor.execute(query)
            conn.commit()

            print(f"Table 'data' created in {config['database']} on {config['host']}")
        except Exception as e:
            print(f"Error creating table in {config['database']}: {e}")
        finally:
            cursor.close()
            conn.close()
            
if __name__ == "__main__":
    create_data_table()
