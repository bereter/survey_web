from typing import Annotated

from fastapi import APIRouter, Form, Body
from .crud import AdminCRUD, QuestionnaireCRUD
from . import schemas


router_admin = APIRouter(prefix='/admin', tags=['Работа с админами'])
router_questionnaire = APIRouter(prefix='/questionnaire', tags=['Работа с опросами'])


@router_admin.get('/', summary='Получить всех админов')
async def get_all_admins():
    return await AdminCRUD.all_data()


@router_admin.post('/', response_model=schemas.Admin)
async def create_admin(items: Annotated[schemas.AdminCreate, Form()]):
    """
    Создание админа
    """
    return await AdminCRUD.create_obj(items=items)


@router_questionnaire.post('/', response_model=schemas.Questionnaire)
async def create_questionnaire(items: schemas.QuestionnaireCreate):
    """
     Создание опроса
    """
    return await QuestionnaireCRUD.create_obj(items=items)