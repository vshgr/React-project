from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.errors import responses
from app.models import Token
from app.services.api.auth import AuthService

router = APIRouter()


@router.get(
    '/auth',
    status_code=200,
    response_model=Token,
    summary="Авторизация пользователя, используя Google OAuth2",
    response_description="Пользователь успешно авторизован, токен возвращен в ответе",
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
async def auth(
    db: AsyncSession = Depends(get_session),
    token: str = Query(..., description="Токен авторизации"),
) -> Token:
    return await AuthService.login(db=db, token=token)
