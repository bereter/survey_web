from api_v1.question import schemas
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models import Question, AnswerAdmin, AnswerUser
from api_v1.crud_basic import BaseCRUD


class QuestionCRUD(BaseCRUD):
    model = Question
    schemas_create = schemas.QuestionCreate
    schemas_return = schemas.Question
    schemas_update = schemas.QuestionUpdate

    @classmethod
    async def get_obj(cls, id_obj: int, session, limit: int = 10, offset: int = 0):
        query = (
            select(cls.model)
            .filter_by(id=id_obj)
            .options(selectinload(cls.model.admin_answer_list), selectinload(cls.model.user_answer_list))
            .limit(limit)
        )
        result: Result = await session.execute(query)
        obj = result.scalars().one_or_none()
        return obj

    @classmethod
    async def create_obj_user(
            cls,
            obj_model: model,
            id_questionnaire: int,
            user_answer_text: str,
            session
    ):
        new_obj = cls.model(
            question_text=obj_model.question_text,
            question_type=obj_model.question_type,
            user_answer_text=user_answer_text,
            questionnaire_id= id_questionnaire,
            )
        session.add(new_obj)
        await session.commit()
        return new_obj


class AnswerAdminCRUD(BaseCRUD):
    model = AnswerAdmin
    schemas_create = schemas.Answer
    schemas_return = schemas.Answer
    schemas_update = schemas.AnswerUpdate


class AnswerUserCRUD(AnswerAdminCRUD):
    model = AnswerUser