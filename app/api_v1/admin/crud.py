from sqlalchemy import select
from app.models import Admin
from . import schemas
from api_v1.crud_basic import SampleCRUD


class AdminCRUD(SampleCRUD):
    model = Admin
    schemas_create = schemas.AdminCreate
    schemas_return = schemas.Admin
    schemas_update = schemas.AdminUpdate

    @classmethod
    async def search_by_email(cls, session, user_email: str) -> model | None:
        query = select(cls.model).filter_by(user_email=user_email)
        result = await session.execute(query)
        return result.scalars().one_or_none()
