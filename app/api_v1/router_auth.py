from typing import Annotated
from fastapi import APIRouter, Form, status, Depends, HTTPException, Response
from api_v1.admin.crud import AdminCRUD
from api_v1.admin import schemas
from app.config import COOKIE_NAME, oauth2_cookie
from app.db import db_halper
from sqlalchemy.ext.asyncio import AsyncSession
from security import verify_password_hash, create_jwt_token, password_hash, verify_jwt_token


router_admin = APIRouter(prefix='/admin', tags=['Регистрация и авторизация админов'])



@router_admin.get('/')
async def get_all_admins(
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> list[schemas.Admin] | None:
    """
    Получить всех админов
    """
    return await AdminCRUD.all_data(session=session)


@router_admin.post('/authorization/')
async def authorization_admin(
        items: Annotated[schemas.AdminAuthorization, Form()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        response: Response
) -> schemas.Admin:
    """
    Авторизация админа
    """
    admin = await AdminCRUD.search_by_email(session=session, user_email=items.user_email)
    if admin:
        password_user = await verify_password_hash(password=items.password, verify_password=admin.password)
        if password_user:
            token = await create_jwt_token(admin)
            response.set_cookie(
                key=COOKIE_NAME,
                value=token,
                httponly=True
            )
            return admin
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    raise HTTPException(status_code=400, detail='Incorrect email or password')


@router_admin.post('/registration/')
async def create_admin(
        items: Annotated[schemas.AdminCreate, Form()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        response: Response
) -> schemas.Admin:
    """
    Регистрация админа
    """
    copy_admin = await AdminCRUD.search_by_email(session=session, user_email=items.user_email)
    if copy_admin:
        raise HTTPException(
            status_code=400,
            detail='User with this email exists'
        )
    items.password = await password_hash(items.password)
    new_admin = await AdminCRUD.create_obj(items=items, session=session)
    token = await create_jwt_token(new_admin)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True
    )
    return new_admin


@router_admin.patch('/{id_admin}/')
async def update_admin(
        id_admin: int,
        items: schemas.AdminUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas.Admin:
    """
     Редактирование админа
    """
    payload = await verify_jwt_token(token=cookie)
    if payload:
        admin = await AdminCRUD.get_obj(id_obj=id_admin, session=session)
        if admin and admin.id == payload.get('id'):
            return await AdminCRUD.update_obj(obj_model=admin, update_model=items, session=session)
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_admin.delete('/{id_admin}/')
async def delete_admin(
        id_admin: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)],
        response: Response
):
    """
     Удаление админа
    """
    payload = await verify_jwt_token(token=cookie)
    if payload:
        obj_delete = await AdminCRUD.get_obj(id_obj=id_admin, session=session)
        if obj_delete.id == payload.get('id'):
            return_bool = await AdminCRUD.delete_obj(model_obj=obj_delete, session=session)
            if return_bool:
                response.delete_cookie(key=COOKIE_NAME)
                return status.HTTP_200_OK
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_404_NOT_FOUND

