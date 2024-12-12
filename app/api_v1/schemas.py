from pydantic import BaseModel, EmailStr, ConfigDict, NaiveDatetime
from datetime import datetime
from app.config import QuestionType


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


class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    question_id: int


class AnswerRead(Answer):
    id: int


class AnswerUpdate(BaseModel):
    text: str | None = None


class QuestionCreate(BaseModel):
    question_text: str
    question_type: QuestionType
    questionnaire_id: int


class Question(QuestionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_answer_text: str | None


class QuestionAllAnswer(Question):
    admin_answer_list: list[AnswerRead] = []
    user_answer_list: list[AnswerRead] = []


class QuestionUpdate(BaseModel):
    question_text: str | None = None
    question_type: str | None = None


class QuestionnaireCreate(BaseModel):
    title: str
    description: str
    date_end: NaiveDatetime | None
    admin_id: int


class QuestionnaireAllQuestions(QuestionnaireCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_parent: int | None
    date_start: datetime
    user: int | None
    questions: list[Question] = []


class Questionnaire(QuestionnaireCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_parent: int| None
    user: int | None
    date_start: datetime


class QuestionnaireUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date_end: datetime | None = None
