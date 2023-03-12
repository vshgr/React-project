from typing import List, Optional, Union

from pydantic import UUID4
from sqlalchemy import BigInteger, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.db.tables.answer import Answer
from app.models import AnswerCreate, AnswerPatch


class AnswerDBService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества ответов"""

        query = select(func.count(Answer.guid)).where(Answer.is_deleted == 0)

        if guids:
            query = query.where(Answer.guid.in_(guids))

        return (await db.execute(query)).scalar()

    @classmethod
    async def exist_one(cls, db: AsyncSession, guid: UUID4) -> Answer:
        """Получение существования ответа"""

        query = select(Answer.guid).where(Answer.guid == guid, Answer.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_one(cls, db: AsyncSession, guid: UUID4) -> Answer:
        """Получение ответа по идентификатору"""

        query = select(Answer).where(Answer.guid == guid, Answer.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_multiple(
        cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int
    ) -> List[Answer]:
        """Получение ответов по идентификаторам"""

        query = select(Answer).where(Answer.is_deleted == 0)

        if guids is not None:
            query = query.where(Answer.guid.in_(guids))

        answers = (await db.execute(query.limit(limit).offset(cast(offset, BigInteger)))).scalars().unique().all()
        return answers

    @classmethod
    async def create(cls, db: AsyncSession, user: UUID4, answer_form: AnswerCreate) -> Answer:
        """Создание ответа"""

        answer = Answer(**answer_form.to_db_dict(user, is_creation=True))
        db.add(answer)
        await db.flush()
        return answer

    @classmethod
    async def update(cls, db: AsyncSession, user: UUID4, guid: UUID4, answer_form: AnswerCreate) -> Answer:
        """Полное обновление ответа"""

        return await cls._change_one(db=db, user=user, guid=guid, answer_form=answer_form)

    @classmethod
    async def patch(cls, db: AsyncSession, user: UUID4, guid: UUID4, answer_form: AnswerPatch) -> Answer:
        """Частичное обновление ответа"""

        return await cls._change_one(db=db, user=user, guid=guid, answer_form=answer_form)

    @classmethod
    async def delete(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление ответа"""

        query = update(Answer).where(Answer.guid == guid).values(is_deleted=1, updated_by=user)
        await db.execute(query)

    @classmethod
    async def _change_one(
        cls, db: AsyncSession, user: UUID4, guid: UUID4, answer_form: Union[AnswerCreate, AnswerPatch]
    ) -> Answer:
        """Общий метод обновления ответов"""

        query = (
            update(Answer).where(Answer.guid == guid).values(**answer_form.dict(exclude_unset=True), updated_by=user)
        )
        await db.execute(query)
        await db.flush()

        return await cls.get_one(db=db, guid=guid)
