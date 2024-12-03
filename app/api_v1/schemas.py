from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class Admin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    user_email: EmailStr
    datetime: datetime


class AdminCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    user_email: EmailStr


class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    question_id: int


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str
    user_answer_text: str | None
    questionnaire_id: int


class Question(QuestionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class QuestionAllAnswer(Question):
    admin_answer_list: list[Answer] = []
    user_answer_list: list[Answer] = []


class QuestionnaireCreate(BaseModel):
    title: str
    description: str
    date_end: datetime | None
    user: int | None
    admin_id: int


class QuestionnaireAllQuestions(QuestionnaireCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_parent: int| None
    date_start: datetime
    questions: list[Question] = []


class Questionnaire(QuestionnaireCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_parent: int| None
    date_start: datetime
