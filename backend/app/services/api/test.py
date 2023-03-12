from typing import List, Optional

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables.test import Test
from app.models import TestCreate, TestGet, TestPatch
from app.services.db.test import TestDBService


class TestService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества тестов"""
        logger.debug(f"Запрос на получение количества тестов, список тестов: {guids =}")

        tests_count = await TestDBService.get_pagination_count(db=db, guids=guids)
        logger.debug(f"Количество тестов: {tests_count}")

        return tests_count

    @classmethod
    async def exist_test(cls, db: AsyncSession, guid: UUID4) -> None:
        """Получение существования теста"""

        logger.debug(f"Запрос на проверку существования тестов: {guid =}")

        test = await TestDBService.exist_one(db=db, guid=guid)
        logger.debug(f"Тест: {test}")

    @classmethod
    async def get_test(cls, db: AsyncSession, guid: UUID4) -> TestGet:
        """Получение теста по идентификатору"""

        logger.debug(f"Запрос на получение тестов: {guid =}")

        test = await cls._get_one(db=db, guid=guid)
        logger.debug(f"Тест получен: {test}")

        return TestGet.from_orm(test)

    @classmethod
    async def get_tests(cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int) -> List[TestGet]:
        """Получение тестов по идентификаторам"""

        logger.debug(f"Запрос на получение списка тестов: {guids =} {limit =} {offset =}")

        db_tests = await TestDBService.get_multiple(db=db, guids=guids, limit=limit, offset=offset)
        logger.debug(f"Тесты получены: {db_tests}")

        return [TestGet.from_orm(test) for test in db_tests]

    @classmethod
    async def create_test(cls, db: AsyncSession, user: UUID4, test_form: TestCreate) -> TestGet:
        """Создание теста"""

        logger.debug(f"Запрос на создание теста: {test_form =}")

        new_test = await TestDBService.create(db=db, user=user, test_form=test_form)
        await db.commit()
        await db.refresh(new_test)

        logger.info(f"Создан новый тест: {new_test = }")

        return TestGet.from_orm(new_test)

    @classmethod
    async def update_test(cls, db: AsyncSession, user: UUID4, guid: UUID4, test_form: TestCreate) -> TestGet:
        """Полное обновление теста"""

        logger.debug(f"Запрос на полное обновление теста {guid = }. Новое значение {test_form =}")

        old_test = await cls._get_one(db=db, guid=guid)
        new_test = await TestDBService.update(db=db, user=user, guid=guid, test_form=test_form)
        await db.commit()
        await db.refresh(new_test)

        logger.info(f"Тест {guid} полностью обновлен. Новое значение {test_form =}. Старое значение {old_test =}")

        return TestGet.from_orm(new_test)

    @classmethod
    async def patch_test(cls, db: AsyncSession, user: UUID4, guid: UUID4, test_form: TestPatch) -> TestGet:
        """Частичное обновление теста"""

        logger.debug(f"Запрос на частичное обновление теста {guid = }. Новое значение {test_form =}")

        old_test = await cls._get_one(db=db, guid=guid)
        new_test = await TestDBService.patch(db=db, user=user, guid=guid, test_form=test_form)
        await db.commit()
        await db.refresh(new_test)

        logger.info(f"Тест {guid} частично обновлен. Новое значение {test_form =}. Старое значение {old_test =}")

        return TestGet.from_orm(new_test)

    @classmethod
    async def delete_test(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление теста"""

        logger.debug(f"Запрос на удаление теста {guid = }")

        await cls._get_one(db=db, guid=guid)
        await TestDBService.delete(db=db, user=user, guid=guid)
        await db.commit()

        logger.info(f"Тест {guid} удален")

    @classmethod
    async def _get_one(cls, db: AsyncSession, guid: UUID4) -> Test:
        """Получение теста по идентификатору и проверка на существование"""

        test = await TestDBService.get_one(db, guid)
        if not test:
            logger.warning(f"Тест {guid} не существует")
            raise HTTPException(status_code=404, detail="Тест не найден")
        return test
