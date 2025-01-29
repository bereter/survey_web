from typing import Annotated
from fastapi import APIRouter, Form, Body, status, Depends, HTTPException, Response, Request, Query
from api_v1.questionnaire.crud import QuestionnaireCRUD
from api_v1.question.crud import QuestionCRUD, AnswerAdminCRUD, AnswerUserCRUD
from api_v1.questionnaire import schemas as schemas_questionnaire
from api_v1.question import schemas as schemas_question
from app.db import db_halper
from sqlalchemy.ext.asyncio import AsyncSession


router_questionnaire_user = APIRouter(prefix='/questionnaire_user', tags=['Прохождение опросов для юзеров'])


@router_questionnaire_user.get('/')
async def get_all_questionnaires_user(
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        user_id: Annotated[int, Query()] | None = None
) -> list[schemas_questionnaire.Questionnaire] | None:
    """
    Получение списка опросов, актуальные для пользователя и пройденные пользователем
    """
    if user_id:
        return await QuestionnaireCRUD.all_data(session=session, user_id=user_id)
    else:
        return await QuestionnaireCRUD.all_data(session=session)


@router_questionnaire_user.get('/{id_questionnaire}/')
async def get_questionnaire_user(
        id_questionnaire: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        user_id: Annotated[int, Query()] | None = None
) -> schemas_questionnaire.QuestionnaireAllQuestions:
    """
    Получение опроса по id для юзера
    """
    questionnaire = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, session=session, user_id=user_id)
    if questionnaire:
        return questionnaire
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_user.get('/question/{id_question}/')
async def get_question_user(
        id_question: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas_question.QuestionAllAnswer:
    """
    Получение вопроса по id для юзера
    """
    question = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
    if question:
        return question
    raise HTTPException(status_code=404, detail='NOT FOUND!')


@router_questionnaire_user.post('/')
async def create_questionnaire_user(
        id_obj: Annotated[int, Body()],
        id_user: Annotated[int, Body()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
) -> schemas_questionnaire.Questionnaire:
    """
     Создание опроса, для юзера
    """
    questionnaire_obj = await QuestionnaireCRUD.get_obj(id_obj=id_obj, session=session)
    return await QuestionnaireCRUD.create_obj_user(obj_model=questionnaire_obj, id_user=id_user, session=session)


@router_questionnaire_user.post('/question/{id_question}/')
async def create_question_user(
        id_question: int,
        id_questionnaire: Annotated[int, Body()],
        id_user: Annotated[int, Body()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        user_text: Annotated[str, Body()] | None = None
):
    """
     Ответ на вопрос от юзера
    """
    questionnaire_obj = await QuestionnaireCRUD.get_obj(id_obj=id_questionnaire, user_id=id_user, session=session)
    if questionnaire_obj:
        question_obj = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
        obj = await QuestionCRUD.create_obj_user(
            obj_model=question_obj,
            id_questionnaire=id_questionnaire,
            user_answer_text=user_text,
            session=session
        )
        if obj:
            return status.HTTP_200_OK

        raise HTTPException(status_code=404, detail='NOT FOUND!')

    raise HTTPException(status_code=404, detail='NOT FOUND!')


# @router_questionnaire_user.post('/question/{id_question}/answer/{id_answer}/')
# async def create_answer_user(
#         id_question: int,
#         id_answer: int,
#         session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
# ):
#
#     """
#     Создание вариантов ответов для юзера
#     """
#
#     # question_obj = await QuestionCRUD.get_obj(id_obj=id_question, session=session)
#
#     answer_obj = await AnswerAdminCRUD.get_obj(id_obj=id_answer, session=session)
#     items = {'text': f'{answer_obj.text}', 'question_id': id_question}
#     create_obj = await AnswerUserCRUD.create_obj(items=items, session=session)