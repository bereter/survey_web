from typing import Annotated
from fastapi import APIRouter, Form, Body, status, Depends, HTTPException, Response, Request
from .crud import AdminCRUD, QuestionnaireCRUD, QuestionCRUD, AnswerAdminCRUD, AnswerUserCRUD
from . import schemas
from app.config import QuestionType, UserOrAdmin, COOKIE_NAME
from app.db import db_halper
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import APIKeyCookie
from security import verify_password_hash, create_access_token, password_hash, verify_token

oauth2_cookie = APIKeyCookie(name=COOKIE_NAME)
router_admin = APIRouter(prefix='/admin', tags=['Работа с админами'])
router_questionnaire = APIRouter(prefix='/questionnaire', tags=['Работа с опросами'])


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
            token = await create_access_token(admin)
            response.set_cookie(
                key=COOKIE_NAME,
                value=token,
                httponly=True
            )
            return admin
        else:
            raise HTTPException(status_code=400, detail='Incorrect email or password')
    else:
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
    token = await create_access_token(new_admin)
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
    payload = await verify_token(token=cookie)
    if payload:
        admin = await AdminCRUD.get_obj(id_obj=id_admin, session=session)
        if admin and admin.id == payload.get('id'):
            return await AdminCRUD.update_obj(obj_model=admin, update_model=items, session=session)
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
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
    payload = await verify_token(token=cookie)
    if payload:
        obj_delete = await AdminCRUD.get_obj(id_obj=id_admin, session=session)
        if obj_delete.id == payload.get('id'):
            return_bool = await AdminCRUD.delete_obj(model_obj=obj_delete, session=session)
            if return_bool:
                response.delete_cookie(key=COOKIE_NAME)
                return status.HTTP_200_OK
            else:
                return status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return status.HTTP_404_NOT_FOUND
    else:
        return status.HTTP_404_NOT_FOUND


@router_questionnaire.get('/{id_questionnaire}/')
async def get_questionnaire(
        id_questionnaire: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.QuestionnaireAllQuestions | None:
    """
    Получение опроса по id
    """
    return await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session)


@router_questionnaire.post('/')
async def create_questionnaire(
        items: schemas.QuestionnaireCreate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas.Questionnaire:
    """
     Создание опроса, для админа
    """
    payload = await verify_token(token=cookie)
    if payload:
        if items.admin_id == payload.get('id'):
            return await QuestionnaireCRUD.create_obj(items=items, session=session)
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
        raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire.patch('/{id_questionnaire}/')
async def update_questionnaire(
        id_questionnaire: int,
        items: schemas.QuestionnaireUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas.Questionnaire:
    """
    Изменение опросника
    """
    obj_update = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session)
    payload = await verify_token(token=cookie)
    if payload and obj_update:
        if obj_update.admin_id == payload.get('id'):
            return await QuestionnaireCRUD.update_obj(obj_model=obj_update, update_model=items, session=session)
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
        raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire.delete('/{id_questionnaire}/')
async def delete_questionnaire(
        id_questionnaire: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
):
    """
    Удаление опроса
    """
    obj_delete = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session)
    payload = await verify_token(token=cookie)
    if payload and obj_delete:
        if obj_delete.admin_id == payload.get('id'):
            return_bool = await QuestionnaireCRUD.delete_obj(model_obj=obj_delete, session=session)
            status_http = status.HTTP_200_OK if return_bool else status.HTTP_500_INTERNAL_SERVER_ERROR
            return status_http
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
        raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire.get('/question/{id_question}/')
async def get_question(
        id_question: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.QuestionAllAnswer | None:
    """
    Получение вопроса по id
    """
    return await QuestionCRUD.get_obj(id_obj=id_question, session=session)


@router_questionnaire.post('/question/')
async def create_question(
        items: schemas.QuestionCreate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas.Question:
    """
    Создание вопроса, для админа

    Значение - question_type: string,
    values: "AT", "CO", "CS"
    """
    payload = await verify_token(token=cookie)
    questionnaire = await QuestionnaireCRUD.get_obj(session=session, id_obj=items.questionnaire_id)
    if payload and questionnaire:
        if payload.get('id') == questionnaire.admin_id:
            return await QuestionCRUD.create_obj(items=items, session=session)
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
        raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire.patch('/question/{id_question}/')
async def update_question(
        id_question: int,
        items: schemas.QuestionUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas.Question:
    """
     Редактирование вопроса
    """
    question = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
    if question:
        questionnaire = await QuestionnaireCRUD.get_obj(session=session, id_obj=question.questionnaire_id)
        payload = await verify_token(token=cookie)
        if payload and questionnaire and question:
            if payload.get('id') == questionnaire.admin_id:
                return await QuestionCRUD.update_obj(obj_model=question, update_model=items, session=session)
            else:
                raise HTTPException(status_code=404, detail='NOT FOUND!')
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
        raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire.delete('/question/{id_question}/')
async def delete_question(
        id_question: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
):
    """
     Удаление вопроса
    """
    question = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
    if question:
        questionnaire = await QuestionnaireCRUD.get_obj(session=session, id_obj=question.questionnaire_id)
        payload = await verify_token(token=cookie)
        if payload and questionnaire and question:
            if payload.get('id') == questionnaire.admin_id:
                return_bool = await QuestionCRUD.delete_obj(model_obj=question, session=session)
                status_http = status.HTTP_200_OK if return_bool else status.HTTP_500_INTERNAL_SERVER_ERROR
                return status_http
            else:
                raise HTTPException(status_code=404, detail='NOT FOUND!')
        else:
            raise HTTPException(status_code=404, detail='NOT FOUND!')
    else:
        raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire.post('/question/answer/')
async def create_answer(
        items: schemas.Answer,
        user_or_admin: UserOrAdmin,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """
    Создание вариантов ответа на вопрос
    """
    if user_or_admin == 'user':

        answer = await AnswerUserCRUD.create_obj(items=items, session=session)
        if answer:
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    elif user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.create_obj(items=items, session=session)
        if answer:
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return status.HTTP_400_BAD_REQUEST


@router_questionnaire.patch('/question/answer/{id_answer}/')
async def update_answer(
        id_answer: int,
        items: schemas.AnswerUpdate,
        user_or_admin: UserOrAdmin,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Answer:
    """
     Редактирование варианта ответа на вопрос
    """
    if user_or_admin == 'user':
        answer = await AnswerUserCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return await AnswerUserCRUD.update_obj(obj_model=answer, update_model=items, session=session)
        else:
            return status.HTTP_404_NOT_FOUND

    elif user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return await AnswerAdminCRUD.update_obj(obj_model=answer, update_model=items, session=session)
        else:
            return status.HTTP_404_NOT_FOUND


@router_questionnaire.delete('/question/answer/{id_answer}/')
async def delete_answer(
        id_answer: int,
        user_or_admin: UserOrAdmin,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """
     Удаление варианта ответа на вопрос
    """
    if user_or_admin == 'user':
        answer = await AnswerUserCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return_bool = await AnswerUserCRUD.delete_obj(model_obj=answer, session=session)
            if return_bool:
                return status.HTTP_200_OK
            else:
                return status.HTTP_500_INTERNAL_SERVER_ERROR

    if user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return_bool = await AnswerAdminCRUD.delete_obj(model_obj=answer, session=session)
            if return_bool:
                return status.HTTP_200_OK
            else:
                return status.HTTP_500_INTERNAL_SERVER_ERROR
