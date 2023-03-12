from pydantic import Field

from app.models.utils import BaseApiModel


class Token(BaseApiModel):
    """Модель токена авторизации"""

    access_token: str = Field(..., description="Токен авторизации")
