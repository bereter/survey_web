from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from api_v1.questionnaire.crud import QuestionnaireCRUD
from api_v1.question.crud import QuestionCRUD, AnswerAdminCRUD, AnswerUserCRUD
from api_v1.questionnaire import schemas as schemas_questionnaire
from api_v1.question import schemas as schemas_question
from app.config import UserOrAdmin, oauth2_cookie
from app.db import db_halper
from sqlalchemy.ext.asyncio import AsyncSession
from security import verify_token


router_questionnaire_admin = APIRouter(
    prefix='/questionnaire_admin',
    tags=['Создание и редактирование опросов админами']
)


@router_questionnaire_admin.get('/{id_questionnaire}/')
async def get_questionnaire_admin(
        id_questionnaire: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas_questionnaire.QuestionnaireAllQuestions:
    """
    Получение опроса админа по id
    """
    payload = await verify_token(token=cookie)

    if payload:
        admin_id = payload.get('id')
        questionnaire = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session, admin_id=admin_id)
        if questionnaire:
            return questionnaire
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.get('/')
async def get_all_questionnaires_admin(
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> list[schemas_questionnaire.Questionnaire] | None:
    """
    Получение списка опросов админа
    """
    payload = await verify_token(token=cookie)
    if payload:
        admin_id = payload.get('id')
        return await QuestionnaireCRUD.all_data(session=session, admin_id=admin_id)
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.post('/')
async def create_questionnaire_admin(
        items: schemas_questionnaire.QuestionnaireCreate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas_questionnaire.Questionnaire:
    """
     Создание опроса, для админа

     Очень важно передавать дату окончания опроса без часового пояса(TimeZone)!!!
    """
    payload = await verify_token(token=cookie)
    if payload:
        if items.admin_id == payload.get('id'):
            return await QuestionnaireCRUD.create_obj(items=items, session=session, admin=True)
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.patch('/{id_questionnaire}/')
async def update_questionnaire(
        id_questionnaire: int,
        items: schemas_questionnaire.QuestionnaireUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas_questionnaire.Questionnaire:
    """
    Изменение опросника
    """
    obj_update = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session)
    payload = await verify_token(token=cookie)
    if payload and obj_update:
        if obj_update.admin_id == payload.get('id'):
            return await QuestionnaireCRUD.update_obj(obj_model=obj_update, update_model=items, session=session)
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.delete('/{id_questionnaire}/')
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
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


# @router_questionnaire_admin.get('/question/{id_question}/')
# async def get_question(
#         id_question: int,
#         session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
# ) -> schemas.QuestionAllAnswer | None:
#     """
#     Получение вопроса по id
#     """
#     question = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
#     if question:
#         return question
#     else:
#         raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.post('/question/')
async def create_question(
        items: schemas_question.QuestionCreate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas_question.Question:
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
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.patch('/question/{id_question}/')
async def update_question(
        id_question: int,
        items: schemas_question.QuestionUpdate,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)]
) -> schemas_question.Question:
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
            raise HTTPException(status_code=404, detail='NOT FOUND!')
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.delete('/question/{id_question}/')
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
            raise HTTPException(status_code=404, detail='NOT FOUND!')
        raise HTTPException(status_code=404, detail='NOT FOUND!')
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_admin.post('/question/answer/')
async def create_answer(
        items: schemas_question.Answer,
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
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    elif user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.create_obj(items=items, session=session)
        if answer:
            return status.HTTP_201_CREATED
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_400_BAD_REQUEST


@router_questionnaire_admin.patch('/question/answer/{id_answer}/')
async def update_answer(
        id_answer: int,
        items: schemas_question.AnswerUpdate,
        user_or_admin: UserOrAdmin,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas_question.Answer:
    """
     Редактирование варианта ответа на вопрос
    """
    if user_or_admin == 'user':
        answer = await AnswerUserCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return await AnswerUserCRUD.update_obj(obj_model=answer, update_model=items, session=session)
        return status.HTTP_404_NOT_FOUND

    elif user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return await AnswerAdminCRUD.update_obj(obj_model=answer, update_model=items, session=session)
        return status.HTTP_404_NOT_FOUND


@router_questionnaire_admin.delete('/question/answer/{id_answer}/')
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
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    if user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.get_obj(id_obj=id_answer, session=session)
        if answer:
            return_bool = await AnswerAdminCRUD.delete_obj(model_obj=answer, session=session)
            if return_bool:
                return status.HTTP_200_OK
            return status.HTTP_500_INTERNAL_SERVER_ERROR