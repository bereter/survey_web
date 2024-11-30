from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


get_db_url = getenv('DB_POSTGRES')