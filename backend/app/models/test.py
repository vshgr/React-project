from datetime import datetime
from typing import Any, Dict, List

from pydantic import UUID4, Field

from app.models.question import QuestionGet
from app.models.utils import BaseApiModel, optional


class TestBase(BaseApiModel):
    """Базовая модель теста"""

    title: str = Field(..., description="Название теста")


class TestGet(TestBase):
    """Модель теста для получения"""

    guid: UUID4 = Field(..., description="Идентификатор теста", alias="id")
    questions: List[QuestionGet] = Field(..., description="Список вопросов в тесте")
    created: datetime = Field(..., description="Момент времени создания объекта в формате RFC-3339")
    updated: datetime = Field(..., description="Момент времени последнего обновления объекта в формате RFC-3339")
    created_by: UUID4 = Field(..., description="Идентификатор пользователя, создавшего объект в системе")
    updated_by: UUID4 = Field(..., description="Идентификатор пользователя, внёсшего последние изменения в объект")

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated = self.updated.replace(microsecond=0)
        self.created = self.created.replace(microsecond=0)


class TestCreate(TestBase):
    """Модель теста для создания или обновления"""

    def to_db_dict(self, user: UUID4, is_creation: bool = False) -> Dict[str, Any]:
        test = self.dict()

        if is_creation:
            test['created_by'] = user
        test['updated_by'] = user

        return test


@optional
class TestPatch(TestCreate):
    """Модель теста для частичного пользователя"""

    pass
