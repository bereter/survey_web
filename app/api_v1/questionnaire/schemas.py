from pydantic import BaseModel, ConfigDict, NaiveDatetime
from datetime import datetime
from api_v1.question.schemas import Question


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
