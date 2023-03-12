from typing import List, Optional

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables.answer import Answer
from app.models import AnswerCreate, AnswerGet, AnswerPatch
from app.services.db.answer import AnswerDBService


class AnswerService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества ответов"""
        logger.debug(f"Запрос на получение количества ответов, список ответов: {guids =}")

        answers_count = await AnswerDBService.get_pagination_count(db=db, guids=guids)
        logger.debug(f"Количество ответов: {answers_count}")

        return answers_count

    @classmethod
    async def exist_answer(cls, db: AsyncSession, guid: UUID4) -> None:
        """Получение существования ответа"""

        logger.debug(f"Запрос на проверку существования ответов: {guid =}")

        answer = await AnswerDBService.exist_one(db=db, guid=guid)
        logger.debug(f"Ответ: {answer}")

    @classmethod
    async def get_answer(cls, db: AsyncSession, guid: UUID4) -> AnswerGet:
        """Получение ответа по идентификатору"""

        logger.debug(f"Запрос на получение ответов: {guid =}")

        answer = await cls._get_one(db=db, guid=guid)
        logger.debug(f"Ответ получен: {answer}")

        return AnswerGet.from_orm(answer)

    @classmethod
    async def get_answers(
        cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int
    ) -> List[AnswerGet]:
        """Получение ответов по идентификаторам"""

        logger.debug(f"Запрос на получение списка ответов: {guids =} {limit =} {offset =}")

        db_answers = await AnswerDBService.get_multiple(db=db, guids=guids, limit=limit, offset=offset)
        logger.debug(f"Ответы получены: {db_answers}")

        return [AnswerGet.from_orm(answer) for answer in db_answers]

    @classmethod
    async def create_answer(cls, db: AsyncSession, user: UUID4, answer_form: AnswerCreate) -> AnswerGet:
        """Создание ответа"""

        logger.debug(f"Запрос на создание ответа: {answer_form =}")

        new_answer = await AnswerDBService.create(db=db, user=user, answer_form=answer_form)
        await db.commit()
        await db.refresh(new_answer)

        logger.info(f"Создан новый ответ: {new_answer = }")

        return AnswerGet.from_orm(new_answer)

    @classmethod
    async def update_answer(cls, db: AsyncSession, user: UUID4, guid: UUID4, answer_form: AnswerCreate) -> AnswerGet:
        """Полное обновление ответа"""

        logger.debug(f"Запрос на полное обновление ответа {guid = }. Новое значение {answer_form =}")

        old_answer = await cls._get_one(db=db, guid=guid)
        new_answer = await AnswerDBService.update(db=db, user=user, guid=guid, answer_form=answer_form)
        await db.commit()
        await db.refresh(new_answer)

        logger.info(f"Ответ {guid} полностью обновлен. Новое значение {answer_form =}. Старое значение {old_answer =}")

        return AnswerGet.from_orm(new_answer)

    @classmethod
    async def patch_answer(cls, db: AsyncSession, user: UUID4, guid: UUID4, answer_form: AnswerPatch) -> AnswerGet:
        """Частичное обновление ответа"""

        logger.debug(f"Запрос на частичное обновление ответа {guid = }. Новое значение {answer_form =}")

        old_answer = await cls._get_one(db=db, guid=guid)
        new_answer = await AnswerDBService.patch(db=db, user=user, guid=guid, answer_form=answer_form)
        await db.commit()
        await db.refresh(new_answer)

        logger.info(f"Ответ {guid} частично обновлен. Новое значение {answer_form =}. Старое значение {old_answer =}")

        return AnswerGet.from_orm(new_answer)

    @classmethod
    async def delete_answer(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление ответа"""

        logger.debug(f"Запрос на удаление ответа {guid = }")

        await cls._get_one(db=db, guid=guid)
        await AnswerDBService.delete(db=db, user=user, guid=guid)
        await db.commit()

        logger.info(f"Ответ {guid} удален")

    @classmethod
    async def _get_one(cls, db: AsyncSession, guid: UUID4) -> Answer:
        """Получение ответа по идентификатору и проверка на существование"""

        answer = await AnswerDBService.get_one(db, guid)
        if not answer:
            logger.warning(f"Ответ {guid} не существует")
            raise HTTPException(status_code=404, detail="Ответ не найден")
        return answer
