from sqlalchemy import select
from typing import Any, Optional, List
from app.db import Base
from pydantic import BaseModel


class BaseCRUD:
    model: Any = Base
    schemas_create: Any = BaseModel
    schemas_return: Any = BaseModel
    schemas_update: Any = BaseModel

    @classmethod
    async def all_data(cls, session) -> List[model] | None:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_obj(cls, id_obj: int, session) -> model | None:
        return await session.get(cls.model, id_obj)


    @classmethod
    async def create_obj(cls, items: schemas_create, session) -> model:
        db = cls.model(**items.model_dump())
        session.add(db)
        await session.commit()
        return db

    @classmethod
    async def update_obj(cls, obj_model: model, update_model: schemas_update, session) -> model:
        for name, value in update_model.model_dump(exclude_unset=True).items():
            setattr(obj_model, name, value)
        await session.commit()
        return obj_model

    @classmethod
    async def delete_obj(cls, model_obj: model, session) -> bool:
        await session.delete(model_obj)
        await session.commit()
        return True