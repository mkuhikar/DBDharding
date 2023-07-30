# db_access.py

import psycopg2
from sharding import get_shard, NUM_SHARDS

# Connection details for each shard (update with your database credentials)
shard_configs = {
	0: {
		'host': 'localhost',
		'user': 'postgres',
		'password': 'qazwsx',
		'database': 'file_shard_0'
	},
	1: {
		'host': 'localhost',
		'user': 'postgres',
		'password': 'qazwsx',
		'database': 'file_shard_1'
	},
	2: {
		'host': 'localhost',
		'user': 'postgres',
		'password': 'qazwsx',
		'database': 'file_shard_2'
	},
}

def get_connection(shard_id):
	
	config = shard_configs[shard_id]
	return psycopg2.connect(**config)



def store_user_file(user_id,i, file_data):
	print(f"Storing: chunk {i}")
	try:
		conn = get_connection(i)
		cursor = conn.cursor()
		query = "INSERT INTO user_file_data (user_id, file_data_chunk) VALUES (%s, %s)"
		cursor.execute(query, (user_id, file_data))
		conn.commit()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	

def retrieve_user_file(user_id, chunk_number):
	if chunk_number < NUM_SHARDS:
		conn = get_connection(chunk_number)
		cursor = conn.cursor()
		query = "SELECT file_data_chunk FROM user_file_data WHERE user_id = %s"
		cursor.execute(query, (user_id,))
		result = cursor.fetchone()
		cursor.close()
		conn.close()
		if result:
			return result[0]
	return None
	

def create_data_table():
	# Loop through all the shards and create the 'data' table in each of them
	for shard_id in range(NUM_SHARDS):
		config = shard_configs[shard_id]

		try:
			conn = psycopg2.connect(**config)
			cursor = conn.cursor()

			# Create the 'data' table if it does not exist
			query = """
			CREATE TABLE IF NOT EXISTS user_file_data (
				user_id VARCHAR(255) PRIMARY KEY,
				file_data_chunk TEXT
			)
			"""
			cursor.execute(query)
			conn.commit()

			print(f"Table 'user_file_data' created in {config['database']} on {config['host']}")
		except Exception as e:
			print(f"Error creating table in {config['database']}: {e}")
		finally:
			cursor.close()
			conn.close()
			
# if __name__ == "__main__":
#     create_data_table()
