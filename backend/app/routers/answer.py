from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.auth import get_user_from_access_token, verify_access_token
from app.db.connection import get_session
from app.errors import responses
from app.models import AnswerCreate, AnswerGet, AnswerPatch
from app.services.api.answer import AnswerService

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    '/answer',
    status_code=201,
    response_model=AnswerGet,
    summary="Создание ответа",
    response_description="Ответ успешно создан и возвращен в ответе",
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
async def create_answer(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    answer_form: AnswerCreate = Body(..., description="Модель создания ответа"),
) -> AnswerGet:
    return await AnswerService.create_answer(db=db, user=user, answer_form=answer_form)


@router.get(
    '/answer',
    status_code=200,
    response_model=list[AnswerGet],
    summary="Получение списка ответов",
    response_description="Список ответов успешно получен и возвращен в ответе",
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
async def get_answers(
    response: Response,
    db: AsyncSession = Depends(get_session),
    ids: Optional[List[UUID4]] = Query(None, description="Идентификаторы ответов"),
    limit: int = Query(30, description="Размер выборки в записях", ge=1, le=1000),
    offset: int = Query(0, description="Смещение в записях относительно начала выборки", ge=0, le=constants.MAX_OFFSET),
) -> list[AnswerGet]:
    count = await AnswerService.get_pagination_count(db=db, guids=ids)
    response.headers[constants.PAGINATION_COUNT] = str(count)
    response.headers[constants.PAGINATION_OFFSET] = str(offset)
    response.headers[constants.PAGINATION_LIMIT] = str(limit)
    return await AnswerService.get_answers(db=db, guids=ids, limit=limit, offset=offset)


@router.get(
    '/answer/{id}',
    status_code=200,
    response_model=AnswerGet,
    summary="Получение ответа по идентификатору",
    response_description="Ответ успешно получен и возвращен в ответе",
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
async def get_answer(
    db: AsyncSession = Depends(get_session),
    id_: UUID4 = Path(..., description="Идентификатор ответа", alias='id'),
) -> AnswerGet:
    return await AnswerService.get_answer(db=db, guid=id_)


@router.put(
    '/answer/{id}',
    status_code=200,
    response_model=AnswerGet,
    summary="Полное обновление ответа по идентификатору",
    response_description="Ответ успешно обновлен и возвращен в ответе",
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
async def update_answer(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор ответа", alias='id'),
    answer_form: AnswerCreate = Body(..., description="Модель полного обновления ответа"),
) -> AnswerGet:
    return await AnswerService.update_answer(db=db, user=user, guid=id_, answer_form=answer_form)


@router.patch(
    '/answer/{id}',
    status_code=200,
    response_model=AnswerGet,
    summary="Частичное обновление ответа по идентификатору",
    response_description="Ответ успешно обновлен и возвращен в ответе",
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
async def patch_answer(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор ответа", alias='id'),
    answer_form: AnswerPatch = Body(..., description="Модель частичного обновления ответа"),
) -> AnswerGet:
    return await AnswerService.patch_answer(db=db, user=user, guid=id_, answer_form=answer_form)


@router.delete(
    '/answer/{id}',
    status_code=204,
    summary="Удаление ответа по идентификатору",
    response_description="Ответ успешно удалена",
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
async def delete_answer(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор ответа", alias='id'),
) -> Response:
    await AnswerService.delete_answer(db=db, user=user, guid=id_)
    return Response(status_code=204)
