from os import getenv
from dotenv import load_dotenv, find_dotenv
from enum import Enum

load_dotenv(find_dotenv())


get_db_url = getenv('DB_POSTGRES')


class QuestionType(str, Enum):
    Answer_Text = "AT"
    Choice_One = "CO"
    Choice_Several = "CS"

class UserOrAdmin(str, Enum):
    user = "user"
    admin = "admin"