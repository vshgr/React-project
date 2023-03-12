from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import UUID4, Field

from app.models.utils import BaseApiModel, optional


class AnswerBase(BaseApiModel):
    """Базовая модель теста"""

    question_guid: UUID4 = Field(..., description="Идентификатор вопроса", alias="questionGuid")
    text: str = Field(..., description="Текст ответа")
    sub_text: Optional[str] = Field(None, description="Доп.текст ответа", alias="subText")
    is_correct: bool = Field(..., description="Признак правильности", alias="isCorrect")


class AnswerGet(AnswerBase):
    """Модель теста для получения"""

    guid: UUID4 = Field(..., description="Идентификатор вопроса", alias="id")
    created: datetime = Field(..., description="Момент времени создания объекта в формате RFC-3339")
    updated: datetime = Field(..., description="Момент времени последнего обновления объекта в формате RFC-3339")
    created_by: UUID4 = Field(..., description="Идентификатор пользователя, создавшего объект в системе")
    updated_by: UUID4 = Field(..., description="Идентификатор пользователя, внёсшего последние изменения в объект")

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated = self.updated.replace(microsecond=0)
        self.created = self.created.replace(microsecond=0)


class AnswerCreate(AnswerBase):
    """Модель теста для создания или обновления"""

    def to_db_dict(self, user: UUID4, is_creation: bool = False) -> Dict[str, Any]:
        answer = self.dict()

        if is_creation:
            answer['created_by'] = user
        answer['updated_by'] = user

        return answer


@optional
class AnswerPatch(AnswerCreate):
    """Модель теста для частичного пользователя"""

    pass
