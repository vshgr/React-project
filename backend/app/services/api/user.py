from typing import List, Optional

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables.user import User
from app.models import UserCreate, UserGet, UserPatch
from app.services.db.user import UserDBService


class UserService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества пользователей"""
        logger.debug(f"Запрос на получение количества пользователей, список пользователей: {guids =}")

        users_count = await UserDBService.get_pagination_count(db=db, guids=guids)
        logger.debug(f"Количество пользователей: {users_count}")

        return users_count

    @classmethod
    async def exist_user(cls, db: AsyncSession, guid: UUID4) -> None:
        """Получение существования пользователя"""

        logger.debug(f"Запрос на проверку существования пользователей: {guid =}")

        user = await UserDBService.exist_one(db=db, guid=guid)
        logger.debug(f"Пользователь: {user}")

    @classmethod
    async def get_user(cls, db: AsyncSession, guid: UUID4) -> UserGet:
        """Получение пользователя по идентификатору"""

        logger.debug(f"Запрос на получение пользователя: {guid =}")

        user = await cls._get_one(db=db, guid=guid)
        logger.debug(f"Пользователь получен: {user}")

        return UserGet.from_orm(user)

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> UserGet:
        """Получение пользователя по email"""

        logger.debug(f"Запрос на получение пользователя: {email =}")

        user = await cls._get_one_by_email(db=db, email=email)
        logger.debug(f"Пользователь получен: {user}")

        return UserGet.from_orm(user)

    @classmethod
    async def get_users(cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int) -> List[UserGet]:
        """Получение пользователей по идентификаторам"""

        logger.debug(f"Запрос на получение списка пользователей: {guids =} {limit =} {offset =}")

        db_users = await UserDBService.get_multiple(db=db, guids=guids, limit=limit, offset=offset)
        logger.debug(f"Пользовательы получены: {db_users}")

        return [UserGet.from_orm(user) for user in db_users]

    @classmethod
    async def create_user(cls, db: AsyncSession, user_form: UserCreate) -> UserGet:
        """Создание пользователя"""

        logger.debug(f"Запрос на создание пользователя: {user_form =}")

        new_user = await UserDBService.create(db=db, user_form=user_form)
        await db.commit()
        await db.refresh(new_user)

        logger.info(f"Создан новый пользователь: {new_user = }")

        return UserGet.from_orm(new_user)

    @classmethod
    async def update_user(cls, db: AsyncSession, user: UUID4, guid: UUID4, user_form: UserCreate) -> UserGet:
        """Полное обновление пользователя"""

        logger.debug(f"Запрос на полное обновление пользователя {guid = }. Новое значение {user_form =}")

        old_user = await cls._get_one(db=db, guid=guid)
        new_user = await UserDBService.update(db=db, guid=guid, user_form=user_form)
        await db.commit()
        await db.refresh(new_user)

        logger.info(
            f"Пользователь {guid} полностью обновлен. Новое значение {user_form =}. Старое значение {old_user =}"
        )

        return UserGet.from_orm(new_user)

    @classmethod
    async def patch_user(cls, db: AsyncSession, user: UUID4, guid: UUID4, user_form: UserPatch) -> UserGet:
        """Частичное обновление пользователя"""

        logger.debug(f"Запрос на частичное обновление пользователя {guid = }. Новое значение {user_form =}")

        old_user = await cls._get_one(db=db, guid=guid)
        new_user = await UserDBService.patch(db=db, guid=guid, user_form=user_form)
        await db.commit()
        await db.refresh(new_user)

        logger.info(
            f"Пользователь {guid} частично обновлен. Новое значение {user_form =}. Старое значение {old_user =}"
        )

        return UserGet.from_orm(new_user)

    @classmethod
    async def delete_user(cls, db: AsyncSession, user: UUID4, guid: UUID4) -> None:
        """Удаление пользователя"""

        logger.debug(f"Запрос на удаление пользователя {guid = }")

        await cls._get_one(db=db, guid=guid)
        await UserDBService.delete(db=db, guid=guid)
        await db.commit()

        logger.info(f"Пользователь {guid} удален")

    @classmethod
    async def _get_one(cls, db: AsyncSession, guid: UUID4) -> User:
        """Получение пользователя по идентификатору и проверка на существование"""

        user = await UserDBService.get_one(db, guid)
        if not user:
            logger.warning(f"Пользователь {guid} не существует")
            raise HTTPException(status_code=404, detail=f"Пользователь {guid} не найден")
        return user

    @classmethod
    async def _get_one_by_email(cls, db: AsyncSession, email: str) -> User:
        """Получение пользователя по email и проверка на существование"""

        user = await UserDBService.get_by_email(db, email)
        if not user:
            logger.warning(f"Пользователь {email} не существует")
            raise HTTPException(status_code=404, detail=f"Пользователь {email} не найден")
        return user
