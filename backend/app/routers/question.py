from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.auth import get_user_from_access_token, verify_access_token
from app.db.connection import get_session
from app.errors import responses
from app.models import QuestionCreate, QuestionGet, QuestionPatch
from app.services.api.question import QuestionService

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    '/question',
    status_code=201,
    response_model=QuestionGet,
    summary="Создание вопроса",
    response_description="Вопрос успешно создан и возвращен в ответе",
    responses={
        400: responses.BAD_REQUEST,
        401: responses.UNAUTHORIZED,
        403: responses.FORBIDDEN,
        404: responses.NOT_FOUND,
        422: responses.UNPROCESSABLE_ENTITY,
        429: responses.TOO_MANY_REQUESTS,
        500: responses.INTERNAL_SERVER_ERROR,
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def create_question(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    question_form: QuestionCreate = Body(..., description="Модель создания вопроса"),
) -> QuestionGet:
    return await QuestionService.create_question(db=db, user=user, question_form=question_form)


@router.get(
    '/question',
    status_code=200,
    response_model=list[QuestionGet],
    summary="Получение списка вопросов",
    response_description="Список вопросов успешно получен и возвращен в ответе",
    responses={
        400: responses.BAD_REQUEST,
        401: responses.UNAUTHORIZED,
        403: responses.FORBIDDEN,
        404: responses.NOT_FOUND,
        422: responses.UNPROCESSABLE_ENTITY,
        429: responses.TOO_MANY_REQUESTS,
        500: responses.INTERNAL_SERVER_ERROR,
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def get_questions(
    response: Response,
    db: AsyncSession = Depends(get_session),
    ids: Optional[List[UUID4]] = Query(None, description="Идентификаторы вопросов"),
    limit: int = Query(30, description="Размер выборки в записях", ge=1, le=1000),
    offset: int = Query(0, description="Смещение в записях относительно начала выборки", ge=0, le=constants.MAX_OFFSET),
) -> list[QuestionGet]:
    count = await QuestionService.get_pagination_count(db=db, guids=ids)
    response.headers[constants.PAGINATION_COUNT] = str(count)
    response.headers[constants.PAGINATION_OFFSET] = str(offset)
    response.headers[constants.PAGINATION_LIMIT] = str(limit)
    return await QuestionService.get_questions(db=db, guids=ids, limit=limit, offset=offset)


@router.get(
    '/question/{id}',
    status_code=200,
    response_model=QuestionGet,
    summary="Получение вопроса по идентификатору",
    response_description="Вопрос успешно получен и возвращен в ответе",
    responses={
        400: responses.BAD_REQUEST,
        401: responses.UNAUTHORIZED,
        403: responses.FORBIDDEN,
        404: responses.NOT_FOUND,
        422: responses.UNPROCESSABLE_ENTITY,
        429: responses.TOO_MANY_REQUESTS,
        500: responses.INTERNAL_SERVER_ERROR,
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def get_question(
    db: AsyncSession = Depends(get_session),
    id_: UUID4 = Path(..., description="Идентификатор вопроса", alias='id'),
) -> QuestionGet:
    return await QuestionService.get_question(db=db, guid=id_)


@router.put(
    '/question/{id}',
    status_code=200,
    response_model=QuestionGet,
    summary="Полное обновление вопроса по идентификатору",
    response_description="Вопрос успешно обновлен и возвращен в ответе",
    responses={
        400: responses.BAD_REQUEST,
        401: responses.UNAUTHORIZED,
        403: responses.FORBIDDEN,
        404: responses.NOT_FOUND,
        422: responses.UNPROCESSABLE_ENTITY,
        429: responses.TOO_MANY_REQUESTS,
        500: responses.INTERNAL_SERVER_ERROR,
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def update_question(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор вопроса", alias='id'),
    question_form: QuestionCreate = Body(..., description="Модель полного обновления вопроса"),
) -> QuestionGet:
    return await QuestionService.update_question(db=db, user=user, guid=id_, question_form=question_form)


@router.patch(
    '/question/{id}',
    status_code=200,
    response_model=QuestionGet,
    summary="Частичное обновление вопроса по идентификатору",
    response_description="Вопрос успешно обновлен и возвращен в ответе",
    responses={
        400: responses.BAD_REQUEST,
        401: responses.UNAUTHORIZED,
        403: responses.FORBIDDEN,
        404: responses.NOT_FOUND,
        422: responses.UNPROCESSABLE_ENTITY,
        429: responses.TOO_MANY_REQUESTS,
        500: responses.INTERNAL_SERVER_ERROR,
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def patch_question(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор вопроса", alias='id'),
    question_form: QuestionPatch = Body(..., description="Модель частичного обновления вопроса"),
) -> QuestionGet:
    return await QuestionService.patch_question(db=db, user=user, guid=id_, question_form=question_form)


@router.delete(
    '/question/{id}',
    status_code=204,
    summary="Удаление вопроса по идентификатору",
    response_description="Вопрос успешно удалена",
    responses={
        400: responses.BAD_REQUEST,
        401: responses.UNAUTHORIZED,
        403: responses.FORBIDDEN,
        404: responses.NOT_FOUND,
        422: responses.UNPROCESSABLE_ENTITY,
        429: responses.TOO_MANY_REQUESTS,
        500: responses.INTERNAL_SERVER_ERROR,
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def delete_question(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор вопроса", alias='id'),
) -> Response:
    await QuestionService.delete_question(db=db, user=user, guid=id_)
    return Response(status_code=204)
