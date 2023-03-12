from typing import List, Optional, Union

from pydantic import UUID4
from sqlalchemy import BigInteger, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.db.tables.question import Question
from app.models import QuestionCreate, QuestionPatch


class QuestionDBService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества вопросов"""

        query = select(func.count(Question.guid)).where(Question.is_deleted == 0)

        if guids:
            query = query.where(Question.guid.in_(guids))

        return (await db.execute(query)).scalar()

    @classmethod
    async def exist_one(cls, db: AsyncSession, guid: UUID4) -> Question:
        """Получение существования вопроса"""

        query = select(Question.guid).where(Question.guid == guid, Question.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_one(cls, db: AsyncSession, guid: UUID4) -> Question:
        """Получение вопроса по идентификатору"""

        query = select(Question).where(Question.guid == guid, Question.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_multiple(
        cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int
    ) -> List[Question]:
        """Получение вопросов по идентификаторам"""

        query = select(Question).where(Question.is_deleted == 0)

        if guids is not None:
            query = query.where(Question.guid.in_(guids))

        questions = (await db.execute(query.limit(limit).offset(cast(offset, BigInteger)))).scalars().unique().all()
        return questions

    @classmethod
    async def create(cls, db: AsyncSession, user: UUID4, question_form: QuestionCreate) -> Question:
        """Создание вопроса"""

        question = Question(**question_form.to_db_dict(user, is_creation=True))
        db.add(question)
        await db.flush()
        return question

    @classmethod
    async def update(cls, db: AsyncSession, user: UUID4, guid: UUID4, question_form: QuestionCreate) -> Question:
        """Полное обновление вопроса"""

        return await cls._change_one(db=db, user=user, guid=guid, question_form=question_form)

    @classmethod
    async def patch(cls, db: AsyncSession, user: UUID4, guid: UUID4, question_form: QuestionPatch) -> Question:
        """Частичное обновление вопроса"""

        return await cls._change_one(db=db, user=user, guid=guid, question_form=question_form)

    @classmethod
    async def delete(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление вопроса"""

        query = update(Question).where(Question.guid == guid).values(is_deleted=1, updated_by=user)
        await db.execute(query)

    @classmethod
    async def _change_one(
        cls, db: AsyncSession, user: UUID4, guid: UUID4, question_form: Union[QuestionCreate, QuestionPatch]
    ) -> Question:
        """Общий метод обновления вопросов"""

        query = (
            update(Question)
            .where(Question.guid == guid)
            .values(**question_form.dict(exclude_unset=True), updated_by=user)
        )
        await db.execute(query)
        await db.flush()

        return await cls.get_one(db=db, guid=guid)
