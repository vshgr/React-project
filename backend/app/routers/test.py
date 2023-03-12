from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.auth import get_user_from_access_token, verify_access_token
from app.db.connection import get_session
from app.errors import responses
from app.models import TestCreate, TestGet, TestPatch
from app.services.api.test import TestService

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    '/test',
    status_code=201,
    response_model=TestGet,
    summary="Создание теста",
    response_description="Тест успешно создан и возвращен в ответе",
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
async def create_test(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    test_form: TestCreate = Body(..., description="Модель создания теста"),
) -> TestGet:
    return await TestService.create_test(db=db, user=user, test_form=test_form)


@router.get(
    '/test',
    status_code=200,
    response_model=list[TestGet],
    summary="Получение списка тестов",
    response_description="Список тестов успешно получен и возвращен в ответе",
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
async def get_tests(
    response: Response,
    db: AsyncSession = Depends(get_session),
    ids: Optional[List[UUID4]] = Query(None, description="Идентификаторы тестов"),
    limit: int = Query(30, description="Размер выборки в записях", ge=1, le=1000),
    offset: int = Query(0, description="Смещение в записях относительно начала выборки", ge=0, le=constants.MAX_OFFSET),
) -> list[TestGet]:
    count = await TestService.get_pagination_count(db=db, guids=ids)
    response.headers[constants.PAGINATION_COUNT] = str(count)
    response.headers[constants.PAGINATION_OFFSET] = str(offset)
    response.headers[constants.PAGINATION_LIMIT] = str(limit)
    return await TestService.get_tests(db=db, guids=ids, limit=limit, offset=offset)


@router.get(
    '/test/{id}',
    status_code=200,
    response_model=TestGet,
    summary="Получение теста по идентификатору",
    response_description="Тест успешно получен и возвращен в ответе",
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
async def get_test(
    db: AsyncSession = Depends(get_session),
    id_: UUID4 = Path(..., description="Идентификатор теста", alias='id'),
) -> TestGet:
    return await TestService.get_test(db=db, guid=id_)


@router.put(
    '/test/{id}',
    status_code=200,
    response_model=TestGet,
    summary="Полное обновление теста по идентификатору",
    response_description="Тест успешно обновлен и возвращен в ответе",
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
async def update_test(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор теста", alias='id'),
    test_form: TestCreate = Body(..., description="Модель полного обновления теста"),
) -> TestGet:
    return await TestService.update_test(db=db, user=user, guid=id_, test_form=test_form)


@router.patch(
    '/test/{id}',
    status_code=200,
    response_model=TestGet,
    summary="Частичное обновление теста по идентификатору",
    response_description="Тест успешно обновлен и возвращен в ответе",
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
async def patch_test(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор теста", alias='id'),
    test_form: TestPatch = Body(..., description="Модель частичного обновления теста"),
) -> TestGet:
    return await TestService.patch_test(db=db, user=user, guid=id_, test_form=test_form)


@router.delete(
    '/test/{id}',
    status_code=204,
    summary="Удаление теста по идентификатору",
    response_description="Тест успешно удалена",
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
async def delete_test(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор теста", alias='id'),
) -> Response:
    await TestService.delete_test(db=db, user=user, guid=id_)
    return Response(status_code=204)
