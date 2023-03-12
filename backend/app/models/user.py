from datetime import datetime
from typing import Any, Dict

from pydantic import UUID4, Field

from app.models.utils import BaseApiModel, optional


class UserBase(BaseApiModel):
    """Базовая модель пользователя"""

    name: str = Field(..., description="Имя пользователя")
    surname: str = Field(..., description="Фамилия пользователя")
    email: str = Field(..., description="Почта пользователя")


class UserGet(UserBase):
    """Модель пользователя для получения"""

    guid: UUID4 = Field(..., description="Идентификатор пользователя", alias="id")
    created: datetime = Field(..., description="Момент времени создания объекта в формате RFC-3339")
    updated: datetime = Field(..., description="Момент времени последнего обновления объекта в формате RFC-3339")

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated = self.updated.replace(microsecond=0)
        self.created = self.created.replace(microsecond=0)


class UserCreate(UserBase):
    """Модель пользователя для создания или обновления"""

    def to_db_dict(self) -> Dict[str, Any]:
        return self.dict()


@optional
class UserPatch(UserCreate):
    """Модель пользователя для частичного пользователя"""

    pass
