from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.auth import get_user_from_access_token, verify_access_token
from app.db.connection import get_session
from app.errors import responses
from app.models import UserCreate, UserGet, UserPatch
from app.services.api.user import UserService

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    '/user',
    status_code=201,
    response_model=UserGet,
    summary="Создание пользователя",
    response_description="Пользователь успешно создан и возвращен в ответе",
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
async def create_user(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    user_form: UserCreate = Body(..., description="Модель создания пользователя"),
) -> UserGet:
    return await UserService.create_user(db=db, user=user, user_form=user_form)


@router.get(
    '/user',
    status_code=200,
    response_model=list[UserGet],
    summary="Получение списка пользователей",
    response_description="Список пользователей успешно получен и возвращен в ответе",
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
async def get_users(
    response: Response,
    db: AsyncSession = Depends(get_session),
    ids: Optional[List[UUID4]] = Query(None, description="Идентификаторы пользователей"),
    limit: int = Query(30, description="Размер выборки в записях", ge=1, le=1000),
    offset: int = Query(0, description="Смещение в записях относительно начала выборки", ge=0, le=constants.MAX_OFFSET),
) -> list[UserGet]:
    count = await UserService.get_pagination_count(db=db, guids=ids)
    response.headers[constants.PAGINATION_COUNT] = str(count)
    response.headers[constants.PAGINATION_OFFSET] = str(offset)
    response.headers[constants.PAGINATION_LIMIT] = str(limit)
    return await UserService.get_users(db=db, guids=ids, limit=limit, offset=offset)


@router.get(
    '/user/{id}',
    status_code=200,
    response_model=UserGet,
    summary="Получение пользователя по идентификатору",
    response_description="Пользователь успешно получен и возвращен в ответе",
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
async def get_user(
    db: AsyncSession = Depends(get_session),
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias='id'),
) -> UserGet:
    return await UserService.get_user(db=db, guid=id_)


@router.get(
    '/user/email/{email}',
    status_code=200,
    response_model=UserGet,
    summary="Получение пользователя по почте",
    response_description="Пользователь успешно получен и возвращен в ответе",
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
async def get_user_by_email(
    db: AsyncSession = Depends(get_session),
    email: str = Path(..., description="Почта пользователя"),
) -> UserGet:
    return await UserService.get_by_email(db=db, email=email)


@router.put(
    '/user/{id}',
    status_code=200,
    response_model=UserGet,
    summary="Полное обновление пользователя по идентификатору",
    response_description="Пользователь успешно обновлен и возвращен в ответе",
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
async def update_user(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias='id'),
    user_form: UserCreate = Body(..., description="Модель полного обновления пользователя"),
) -> UserGet:
    return await UserService.update_user(db=db, user=user, guid=id_, user_form=user_form)


@router.patch(
    '/user/{id}',
    status_code=200,
    response_model=UserGet,
    summary="Частичное обновление пользователя по идентификатору",
    response_description="Пользователь успешно обновлен и возвращен в ответе",
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
async def patch_user(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias='id'),
    user_form: UserPatch = Body(..., description="Модель частичного обновления пользователя"),
) -> UserGet:
    return await UserService.patch_user(db=db, user=user, guid=id_, user_form=user_form)


@router.delete(
    '/user/{id}',
    status_code=204,
    summary="Удаление пользователя по идентификатору",
    response_description="Пользователь успешно удалена",
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
async def delete_user(
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(get_user_from_access_token),
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias='id'),
) -> Response:
    await UserService.delete_user(db=db, user=user, guid=id_)
    return Response(status_code=204)
