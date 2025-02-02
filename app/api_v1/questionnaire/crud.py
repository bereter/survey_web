from . import schemas
from app.models import Questionnaire
from datetime import datetime
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from api_v1.crud_basic import BaseCRUD


class QuestionnaireCRUD(BaseCRUD):
    model = Questionnaire
    schemas_create = schemas.QuestionnaireCreate
    schemas_return = schemas.Questionnaire
    schemas_update = schemas.QuestionnaireUpdate

    @classmethod
    async def create_obj_user(cls, obj_model: model, id_user: int, session):
        new_obj = cls.model(
            admin_id=obj_model.admin_id,
            user=id_user,
            title=obj_model.title,
            description= obj_model.description,
            date_end=obj_model.date_end,
            id_parent=obj_model.id_parent
            )
        session.add(new_obj)
        await session.commit()
        return new_obj

    @classmethod
    async def all_data(cls,
                       session,
                       user_id: int = None,
                       admin_id: int = None,
                       limit: int = 10,
                       offset: int = 0,
                       all_questionnaire_users: bool = False
                       ) -> list[model] | None:
        if admin_id and not user_id and not all_questionnaire_users:
            query = (select(cls.model)
                     .filter_by(admin_id=admin_id, user=None)
                     .order_by(cls.model.date_start.desc())
                     .limit(limit)
                     .offset(offset))
            result = await session.execute(query)
            return result.scalars().all()
        elif not admin_id and user_id and not all_questionnaire_users:
            query = select(cls.model).filter_by(user=user_id).limit(limit).offset(offset)
            result = await session.execute(query)
            return result.scalars().all()
        elif not admin_id and not user_id and all_questionnaire_users:
            query = (select(cls.model)
                     .filter(cls.model.user != None)
                     .order_by(cls.model.date_start.desc())
                     .limit(limit)
                     .offset(offset)
                     )
            result = await session.execute(query)
            return result.scalars().all()
        else:
            query = select(cls.model).filter_by(user=None).filter(cls.model.date_end > datetime.now())
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create_obj(cls, items: schemas_create, session, admin: bool = False) -> model:
        db = cls.model(**items.model_dump())
        session.add(db)
        await session.commit()
        if admin:
            setattr(db, 'id_parent', db.id)
            await session.commit()
            return db
        else:
            return db

    @classmethod
    async def get_obj(cls,
                      id_obj: int,
                      session, limit: int = 10,
                      offset: int = 0,
                      admin_id: int = None,
                      user_id: int = None
                      ) -> model | None:
        if admin_id:
            query = (
                select(cls.model)
                .filter_by(id=id_obj, admin_id=admin_id)
                .options(selectinload(cls.model.questions))
                .limit(limit)
                .offset(offset)
            )
            result: Result = await session.execute(query)
            obj = result.scalars().one_or_none()
            return obj
        else:
            query = (
                select(cls.model)
                .filter(cls.model.date_end > datetime.now())
                .filter_by(id=id_obj, user=user_id)
                .options(selectinload(cls.model.questions))
                .limit(limit)
                .offset(offset)
            )
            result: Result = await session.execute(query)
            obj = result.scalars().one_or_none()
            return obj
