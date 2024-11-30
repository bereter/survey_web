from datetime import datetime, date

from sqlalchemy import select
from app.db import async_session_maker
from app.models import Admin, AnswerAdmin, AnswerUser, Question, Questionnaire
from . import schemas


class AdminCRUD:
    model = Admin
    schemas_create = schemas.AdminCreate

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
    async def create_obj(cls, items: schemas_create):
        async with async_session_maker() as session:
            db_admin = cls.model(**items.model_dump())
            session.add(db_admin)
            await session.commit()
            return db_admin


class QuestionnaireCRUD(AdminCRUD):
    model = Questionnaire
    schemas_create = schemas.QuestionnaireCreate


    @classmethod
    async def create_obj(cls, items: schemas_create):
        async with async_session_maker() as session:
            print(items.date_end)
            print(datetime.now())
            items.date_end = datetime.now()
            db_admin = cls.model(**items.model_dump())
            session.add(db_admin)
            await session.commit()
            return db_admin
