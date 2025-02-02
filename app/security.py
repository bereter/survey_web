import jwt
from passlib.context import CryptContext
from config import JWT_SECRET


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



# хеширование пароля
async def password_hash(password):
    return pwd_context.hash(password)


# расшифровка пароля
async def verify_password_hash(password, verify_password):
    return pwd_context.verify(password, verify_password)


# создание токена
async def create_jwt_token(admin):
    try:
        payload = {
            'id': admin.id,
            'username': admin.username,
            'user_email': admin.user_email,

        }
        return jwt.encode(payload, key=JWT_SECRET, algorithm='HS256')
    except Exception as ex:
        print(ex)
        return None


# расшифровка токена
async def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms='HS256')
        return payload
    except Exception as ex:
        print(str(ex))
        return None
