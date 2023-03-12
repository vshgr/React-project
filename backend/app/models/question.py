from datetime import datetime
from typing import Any, Dict, List

from pydantic import UUID4, Field

from app.models.answer import AnswerGet
from app.models.utils import BaseApiModel, optional


class QuestionBase(BaseApiModel):
    """Базовая модель теста"""

    test_guid: UUID4 = Field(..., description="Идентификатор теста", alias="testGuid")
    title: str = Field(..., description="Название вопроса")
    type: str = Field(..., description="Тип вопроса")


class QuestionGet(QuestionBase):
    """Модель теста для получения"""

    guid: UUID4 = Field(..., description="Идентификатор ответа", alias="id")
    answers: List[AnswerGet] = Field(..., description="Список ответов в вопросе")
    created: datetime = Field(..., description="Момент времени создания объекта в формате RFC-3339")
    updated: datetime = Field(..., description="Момент времени последнего обновления объекта в формате RFC-3339")
    created_by: UUID4 = Field(..., description="Идентификатор пользователя, создавшего объект в системе")
    updated_by: UUID4 = Field(..., description="Идентификатор пользователя, внёсшего последние изменения в объект")

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated = self.updated.replace(microsecond=0)
        self.created = self.created.replace(microsecond=0)


class QuestionCreate(QuestionBase):
    """Модель теста для создания или обновления"""

    def to_db_dict(self, user: UUID4, is_creation: bool = False) -> Dict[str, Any]:
        question = self.dict()

        if is_creation:
            question['created_by'] = user
        question['updated_by'] = user

        return question


@optional
class QuestionPatch(QuestionCreate):
    """Модель теста для частичного пользователя"""

    pass
