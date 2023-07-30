# Local File Storage with PostgreSQL Sharding

## Overview
This project implements a local file storage system inspired by cloud-based platforms like Dropbox and Google Drive. The goal is to read a file, distribute its contents across multiple PostgreSQL databases using database sharding principles, retrieve the stored data, reconstruct the original file, and save it in an output folder.

## Project Features
- Read a file and divide it into smaller chunks for efficient storage.
- Employ database sharding to distribute chunks across multiple PostgreSQL databases.
- Retrieve and reconstruct the original file from stored chunks.
- Save the recreated file to an output folder for easy access.

## Setup Instructions
1. Clone the repository to your local machine.
2. Ensure you have PostgreSQL installed and running.
3. Install the required Python dependencies using `pip install -r requirements.txt`.
4. Adjust the database connection configuration in the `db_access.py` file.
5. Run the project using `python app.py`.

## Project Structure
- `app.py`: The main script to run the file storage and retrieval process.
- `db_access.py`: Provides database access functions for storing and retrieving chunks.
- `user_data`: Directory to store the input file (e.g., "SelfieLeLeRe.mp3").
- `output`: Directory to save the recreated file (e.g., "SelfieLeLeRe.mp3").

## Usage
1. Place your input file (e.g., "SelfieLeLeRe.mp3") in the `user_data` folder.
2. Run the `app.py` script to store the file in sharded databases and recreate the file.
3. The recreated file will be saved in the `output` folder with the name "SelfieLeLeRe.mp3".

## Notes
- The project uses the `psycopg2` library for PostgreSQL database access.
- The default chunk size is set to 5 MB, but you can adjust it in the `app.py` file.
- Ensure you have sufficient database access permissions and update the configuration accordingly.

## License
This project is licensed under the [MIT License](LICENSE).

Feel free to contribute, report issues, or suggest improvements!

