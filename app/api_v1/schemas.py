from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date


class Admin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    user_email: EmailStr
    datetime: datetime


class AdminCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    user_email: EmailStr


class Questionnaire(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    date_start: datetime
    date_end: datetime | None = None
    admin_id: int


class QuestionnaireCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    date_end: datetime | None
    user: int | None
    admin_id: int