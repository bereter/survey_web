from typing import Annotated

from fastapi import APIRouter, Form, Body, status

from .crud import AdminCRUD, QuestionnaireCRUD, QuestionCRUD, AnswerAdminCRUD, AnswerUserCRUD
from . import schemas


router_admin = APIRouter(prefix='/admin', tags=['Работа с админами'])
router_questionnaire = APIRouter(prefix='/questionnaire', tags=['Работа с опросами'])


@router_admin.get('/', summary='Получить всех админов')
async def get_all_admins() -> list[schemas.Admin] | None:
    return await AdminCRUD.all_data()


@router_admin.post('/', response_model=schemas.Admin)
async def create_admin(items: Annotated[schemas.AdminCreate, Form()]):
    """
    Создание админа
    """
    return await AdminCRUD.create_obj(items=items)


@router_questionnaire.get('/{id_questionnaire}/')
async def get_questionnaire(id_questionnaire: int) -> schemas.QuestionnaireAllQuestions | None:
    """
    Получение опроса по id
    """
    return await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire)


@router_questionnaire.post('/')
async def create_questionnaire(items: schemas.QuestionnaireCreate) -> schemas.Questionnaire:
    """
     Создание опроса
    """
    return await QuestionnaireCRUD.create_obj(items=items)


@router_questionnaire.get('/question/{id_question}/')
async def get_question(id_question: int) -> schemas.QuestionAllAnswer | None:
    """
    Получение вопроса по id
    """
    return await QuestionCRUD.get_obj(id_obj=id_question)


@router_questionnaire.post('/question/')
async def create_question(items: schemas.QuestionCreate) -> schemas.Question:
    """
    Создание вопроса
    """
    return await QuestionCRUD.create_obj(items=items)


@router_questionnaire.post('/question/answer/{user_or_admin}/')
async def create_answer(items: schemas.Answer, user_or_admin: str):
    """
    Создание вариантов ответа на вопрос
    """
    if user_or_admin == 'user':

        answer = await AnswerUserCRUD.create_obj(items=items)
        if answer:
            return status.HTTP_201_CREATED
        else: return status.HTTP_500_INTERNAL_SERVER_ERROR

    elif user_or_admin == 'admin':
        answer = await AnswerAdminCRUD.create_obj(items=items)
        if answer:
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
    else: return status.HTTP_400_BAD_REQUEST