from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class Admin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    user_email: EmailStr
    datetime: datetime


class AdminCreate(BaseModel):
    username: str
    password: str
    user_email: EmailStr


class AdminUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


class AdminAuthorization(BaseModel):
    user_email: EmailStr
    password: str