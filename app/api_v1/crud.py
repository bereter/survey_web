from datetime import datetime
from sqlalchemy.engine import Result
from sqlalchemy.orm import contains_eager, selectinload
from sqlalchemy import select
from app.db import async_session_maker
from app.models import Admin, AnswerAdmin, AnswerUser, Question, Questionnaire
from . import schemas


class AdminCRUD:
    model = Admin
    schemas_create = schemas.AdminCreate
    schemas_return = schemas.Admin

    @classmethod
    async def all_data(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def get_obj(cls, id_obj: int):
        async with async_session_maker() as session:
            return await session.get(cls.model, id_obj)


    @classmethod
    async def create_obj(cls, items: schemas_create) -> schemas_return:
        async with async_session_maker() as session:
            db = cls.model(**items.model_dump())
            session.add(db)
            await session.commit()
            return db


class QuestionnaireCRUD(AdminCRUD):
    model = Questionnaire
    schemas_create = schemas.QuestionnaireCreate
    schemas_return = schemas.Questionnaire


    @classmethod
    async def create_obj(cls, items: schemas_create) -> schemas_return:
        async with async_session_maker() as session:
            items.date_end = None
            # if items.user in None:
            #     items.id_start = items.id
            # items.id_parent = items.id
            db = cls.model(**items.model_dump())
            session.add(db)
            await session.commit()
            return db


    @classmethod
    async def get_obj(cls, id_obj: int, limit: int = 10, offset: int = 0):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=id_obj)
                .options(selectinload(cls.model.questions))
                .limit(limit)
            )
            result: Result = await session.execute(query)
            obj = result.scalars().one_or_none()
            return obj


class QuestionCRUD(AdminCRUD):
    model = Question
    schemas_create = schemas.QuestionCreate
    schemas_return = schemas.Question

    @classmethod
    async def get_obj(cls, id_obj: int, limit: int = 10, offset: int = 0):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=id_obj)
                .options(selectinload(cls.model.admin_answer_list), selectinload(cls.model.user_answer_list))
                .limit(limit)
            )
            result: Result = await session.execute(query)
            obj = result.scalars().one_or_none()
            return obj


class AnswerAdminCRUD(AdminCRUD):
    model = AnswerAdmin
    schemas_create = schemas.Answer
    schemas_return = schemas.Answer


class AnswerUserCRUD(AnswerAdminCRUD):
    model = AnswerUser


