from typing import List, Optional, Union

from pydantic import UUID4
from sqlalchemy import BigInteger, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql.expression import cast

from app.db import Question
from app.db.tables.test import Test
from app.models import TestCreate, TestPatch


class TestDBService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества тестов"""

        query = select(func.count(Test.guid)).where(Test.is_deleted == 0)

        if guids:
            query = query.where(Test.guid.in_(guids))

        return (await db.execute(query)).scalar()

    @classmethod
    async def exist_one(cls, db: AsyncSession, guid: UUID4) -> Test:
        """Получение существования теста"""

        query = select(Test.guid).where(Test.guid == guid, Test.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_one(cls, db: AsyncSession, guid: UUID4) -> Test:
        """Получение теста по идентификатору"""

        query = select(Test).where(Test.guid == guid, Test.is_deleted == 0)\
            .join(Test.questions)\
            .options(contains_eager(Test.questions))\
            .where(Question.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_multiple(cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int) -> List[Test]:
        """Получение тестов по идентификаторам"""

        query = select(Test).where(Test.is_deleted == 0)\
            .join(Test.questions)\
            .options(contains_eager(Test.questions))\
            .where(Question.is_deleted == 0)

        if guids is not None:
            query = query.where(Test.guid.in_(guids))

        tests = (await db.execute(query.limit(limit).offset(cast(offset, BigInteger)))).scalars().unique().all()
        return tests

    @classmethod
    async def create(cls, db: AsyncSession, user: UUID4, test_form: TestCreate) -> Test:
        """Создание теста"""

        test = Test(**test_form.to_db_dict(user, is_creation=True))
        db.add(test)
        await db.flush()
        return test

    @classmethod
    async def update(cls, db: AsyncSession, user: UUID4, guid: UUID4, test_form: TestCreate) -> Test:
        """Полное обновление теста"""

        return await cls._change_one(db=db, user=user, guid=guid, test_form=test_form)

    @classmethod
    async def patch(cls, db: AsyncSession, user: UUID4, guid: UUID4, test_form: TestPatch) -> Test:
        """Частичное обновление теста"""

        return await cls._change_one(db=db, user=user, guid=guid, test_form=test_form)

    @classmethod
    async def delete(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление теста"""

        query = update(Test).where(Test.guid == guid).values(is_deleted=1, updated_by=user)
        await db.execute(query)

    @classmethod
    async def _change_one(
        cls, db: AsyncSession, user: UUID4, guid: UUID4, test_form: Union[TestCreate, TestPatch]
    ) -> Test:
        """Общий метод обновления тестов"""

        query = update(Test).where(Test.guid == guid).values(**test_form.dict(exclude_unset=True), updated_by=user)
        await db.execute(query)
        await db.flush()

        return await cls.get_one(db=db, guid=guid)
