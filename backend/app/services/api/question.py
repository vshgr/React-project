from typing import List, Optional

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables.question import Question
from app.models import QuestionCreate, QuestionGet, QuestionPatch
from app.services.db.question import QuestionDBService


class QuestionService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества вопросов"""
        logger.debug(f"Запрос на получение количества вопросов, список вопросов: {guids =}")

        questions_count = await QuestionDBService.get_pagination_count(db=db, guids=guids)
        logger.debug(f"Количество вопросов: {questions_count}")

        return questions_count

    @classmethod
    async def exist_question(cls, db: AsyncSession, guid: UUID4) -> None:
        """Получение существования вопроса"""

        logger.debug(f"Запрос на проверку существования вопросов: {guid =}")

        question = await QuestionDBService.exist_one(db=db, guid=guid)
        logger.debug(f"Вопрос: {question}")

    @classmethod
    async def get_question(cls, db: AsyncSession, guid: UUID4) -> QuestionGet:
        """Получение вопроса по идентификатору"""

        logger.debug(f"Запрос на получение вопросов: {guid =}")

        question = await cls._get_one(db=db, guid=guid)
        logger.debug(f"Вопрос получен: {question}")

        return QuestionGet.from_orm(question)

    @classmethod
    async def get_questions(
        cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int
    ) -> List[QuestionGet]:
        """Получение вопросов по идентификаторам"""

        logger.debug(f"Запрос на получение списка вопросов: {guids =} {limit =} {offset =}")

        db_questions = await QuestionDBService.get_multiple(db=db, guids=guids, limit=limit, offset=offset)
        logger.debug(f"Вопросы получены: {db_questions}")

        return [QuestionGet.from_orm(question) for question in db_questions]

    @classmethod
    async def create_question(cls, db: AsyncSession, user: UUID4, question_form: QuestionCreate) -> QuestionGet:
        """Создание вопроса"""

        logger.debug(f"Запрос на создание вопроса: {question_form =}")

        new_question = await QuestionDBService.create(db=db, user=user, question_form=question_form)
        await db.commit()
        await db.refresh(new_question)

        logger.info(f"Создан новый вопрос: {new_question = }")

        return QuestionGet.from_orm(new_question)

    @classmethod
    async def update_question(
        cls, db: AsyncSession, user: UUID4, guid: UUID4, question_form: QuestionCreate
    ) -> QuestionGet:
        """Полное обновление вопроса"""

        logger.debug(f"Запрос на полное обновление вопроса {guid = }. Новое значение {question_form =}")

        old_question = await cls._get_one(db=db, guid=guid)
        new_question = await QuestionDBService.update(db=db, user=user, guid=guid, question_form=question_form)
        await db.commit()
        await db.refresh(new_question)

        logger.info(
            f"Вопрос {guid} полностью обновлен. Новое значение {question_form =}. Старое значение {old_question =}"
        )

        return QuestionGet.from_orm(new_question)

    @classmethod
    async def patch_question(
        cls, db: AsyncSession, user: UUID4, guid: UUID4, question_form: QuestionPatch
    ) -> QuestionGet:
        """Частичное обновление вопроса"""

        logger.debug(f"Запрос на частичное обновление вопроса {guid = }. Новое значение {question_form =}")

        old_question = await cls._get_one(db=db, guid=guid)
        new_question = await QuestionDBService.patch(db=db, user=user, guid=guid, question_form=question_form)
        await db.commit()
        await db.refresh(new_question)

        logger.info(
            f"Вопрос {guid} частично обновлен. Новое значение {question_form =}. Старое значение {old_question =}"
        )

        return QuestionGet.from_orm(new_question)

    @classmethod
    async def delete_question(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление вопроса"""

        logger.debug(f"Запрос на удаление вопроса {guid = }")

        await cls._get_one(db=db, guid=guid)
        await QuestionDBService.delete(db=db, user=user, guid=guid)
        await db.commit()

        logger.info(f"Вопрос {guid} удален")

    @classmethod
    async def _get_one(cls, db: AsyncSession, guid: UUID4) -> Question:
        """Получение вопроса по идентификатору и проверка на существование"""

        question = await QuestionDBService.get_one(db, guid)
        if not question:
            logger.warning(f"Вопрос {guid} не существует")
            raise HTTPException(status_code=404, detail="Вопрос не найден")
        return question
