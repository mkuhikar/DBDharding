#app.py

import os
import math
from db_access import store_user_file
import hashlib
from db_access import retrieve_user_file


def chunk_file(file_path, chunk_size):
	with open(file_path, 'rb') as file:
		while True:
			data_chunk = file.read(chunk_size)
			if not data_chunk:
				break
			yield data_chunk

def generate_unique_user_id(file_path, chunk_number):
	# Concatenate the file path and chunk number to create a unique identifier
	unique_identifier = f"{file_path}{chunk_number}"
	# Compute the SHA-256 hash of the unique identifier to generate the user_id
	return hashlib.sha256(unique_identifier.encode('utf-8')).hexdigest()

def store_file_in_shards(user_id, file_path, chunk_size=5 * 1024 * 1024):
	for i, chunk in enumerate(chunk_file(file_path, chunk_size)):
		 # Generate a unique user_id for each chunk
		unique_user_id = generate_unique_user_id(file_path, i)
		store_user_file(unique_user_id, i, chunk)

def recreate_file(file_path, output_file_path):
	# Initialize an empty bytearray to hold the file data
	file_data = bytearray()
	# Start with chunk_number 0 and keep fetching chunks until None is returned
	chunk_number = 0
	
	
	while True:
		# Construct the user_id for the current chunk
		current_user_id = generate_unique_user_id(file_path,chunk_number)

		# Retrieve the chunk from the database
		chunk_data = retrieve_user_file(current_user_id, chunk_number)
		if chunk_data:
			# Append the retrieved chunk to the file_data bytearray
			file_data += chunk_data
		else:
			# No more chunks found for the user_id, break the loop
			break

		# Move to the next chunk
		chunk_number += 1

	# Save the recreated file to the output_file_path
	with open(output_file_path, 'wb') as file:
		file.write(file_data)

if __name__ == "__main__":
	user_id = "user_1234561"
	script_directory = os.path.dirname(os.path.abspath(__file__))

	# Get the path to the music file (Selfie.mp3)
	file_path = os.path.join(script_directory, "user_data", "SelfieLeLeRe.mp3")
	filename = os.path.basename(file_path)

	output_path = os.path.join(script_directory,"output",filename)
	

	# Check if the file exists
	if not os.path.exists(file_path):
		print(f"File '{file_path}' not found.")
	else:
		# Calculate the total file size
		total_file_size = os.path.getsize(file_path)
		print(f"Total File Size: {total_file_size} bytes")

		# Set the chunk size to 5MB
		chunk_size = 5 * 1024 * 1024

		# Calculate the number of chunks required
		num_chunks = math.ceil(total_file_size / chunk_size)
		print(f"Number of Chunks: {num_chunks}")

		# Store each chunk in different shards using sharding
		store_file_in_shards(user_id, file_path, chunk_size)
		print("File stored in shards successfully.")
		recreate_file(file_path,output_path)
		print("File recreated from shards successfully.")


