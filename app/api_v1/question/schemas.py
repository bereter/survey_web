from pydantic import BaseModel, ConfigDict
from app.config import QuestionType


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