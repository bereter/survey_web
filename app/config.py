from os import getenv
from dotenv import load_dotenv, find_dotenv
from enum import Enum
from fastapi.security import APIKeyCookie


load_dotenv(find_dotenv())

get_db_url = getenv('DB_POSTGRES')
COOKIE_NAME = 'Authorization'
JWT_SECRET = getenv('JWT_SECRET_KEY')
oauth2_cookie = APIKeyCookie(name=COOKIE_NAME)


class QuestionType(str, Enum):
    Answer_Text = "AT"
    Choice_One = "CO"
    Choice_Several = "CS"

class UserOrAdmin(str, Enum):
    user = "user"
    admin = "admin"

