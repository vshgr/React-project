from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.errors import responses
from app.utils import check_db

router = APIRouter()


@router.get(
    "/health",
    status_code=204,
    summary="Проверка доступности сервиса",
    response_description="Сервис доступен",
    responses={
        503: responses.SERVICE_UNAVAILABLE,
    },
)
@router.head(
    "/health",
    status_code=204,
    summary="Проверка доступности сервиса",
    response_description="Сервис доступен",
    responses={
        503: responses.SERVICE_UNAVAILABLE,
    },
)
async def health_check(db: AsyncSession = Depends(get_session)) -> Response:
    if not await check_db(db):
        return Response(status_code=503, content="Сервис недоступен, не удалось подключиться к базе данных")
    return Response(status_code=204)
