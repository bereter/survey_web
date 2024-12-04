from typing import Annotated
from fastapi import APIRouter, Form, Body, status, Depends
from .crud import AdminCRUD, QuestionnaireCRUD, QuestionCRUD, AnswerAdminCRUD, AnswerUserCRUD
from . import schemas
from app.config import QuestionType, UserOrAdmin
from app.db import db_halper
from sqlalchemy.ext.asyncio import AsyncSession

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


@router_admin.get('/{id_admin}/')
async def get_admin(
        id_admin: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Admin | None:
    """
    Получить админа
    """
    return await AdminCRUD.get_obj(id_obj=id_admin, session=session)


@router_admin.post('/', response_model=schemas.Admin)
async def create_admin(
        items: Annotated[schemas.AdminCreate, Form()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """
    Создание админа
    """
    return await AdminCRUD.create_obj(items=items, session=session)


@router_admin.patch('/{id_admin}/')
async def update_admin(
        id_admin: int,
        items: schemas.AdminUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Admin:
    """
     Редактирование админа
    """
    admin = await AdminCRUD.get_obj(id_obj=id_admin, session=session)
    if admin:
        return await AdminCRUD.update_obj(obj_model=admin, update_model=items, session=session)
    else:
        return status.HTTP_404_NOT_FOUND


@router_admin.delete('/{id_admin}/')
async def delete_admin(
    id_admin: int,
    session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """
     Удаление админа
    """
    obj_delete = await AdminCRUD.get_obj(id_obj=id_admin, session=session)
    return_bool = await AdminCRUD.delete_obj(model_obj=obj_delete, session=session)
    if return_bool:
        return status.HTTP_200_OK
    else:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


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
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Questionnaire:
    """
     Создание опроса
    """
    return await QuestionnaireCRUD.create_obj(items=items, session=session)


@router_questionnaire.patch('/{id_questionnaire}/')
async def update_questionnaire(
        id_questionnaire: int,
        items: schemas.QuestionnaireUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Questionnaire:
    """
    Изменение опросника
    """
    obj_update = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session)
    if obj_update:
        return await QuestionnaireCRUD.update_obj(obj_model=obj_update, update_model=items, session=session)


@router_questionnaire.delete('/{id_questionnaire}/')
async def delete_questionnaire(
        id_questionnaire: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """
    Удаление опроса
    """
    obj_delete = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session)
    return_bool = await QuestionnaireCRUD.delete_obj(model_obj=obj_delete, session=session)
    if return_bool:
        return status.HTTP_200_OK
    else:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


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
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Question:
    """
    Создание вопроса

    Значение - question_type: string,
    values: "AT", "CO", "CS"
    """
    return await QuestionCRUD.create_obj(items=items, session=session)



@router_questionnaire.patch('/question/{id_question}/')
async def update_question(
        id_question: int,
        items: schemas.QuestionUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas.Question:
    """
     Редактирование вопроса
    """
    question = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
    if question:
        return await QuestionCRUD.update_obj(obj_model=question, update_model=items, session=session)
    else:
        return status.HTTP_404_NOT_FOUND


@router_questionnaire.delete('/question/{id_question}/')
async def delete_admin(
    id_question: int,
    session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """
     Удаление вопроса
    """
    question = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
    return_bool = await QuestionCRUD.delete_obj(model_obj=question, session=session)
    if return_bool:
        return status.HTTP_200_OK
    else:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


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