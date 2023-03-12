from typing import List, Optional, Union

from pydantic import UUID4
from sqlalchemy import BigInteger, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.db.tables.user import User
from app.models import UserCreate, UserPatch


class UserDBService:
    @classmethod
    async def get_pagination_count(cls, db: AsyncSession, guids: Optional[List[UUID4]]) -> int:
        """Получение количества пользователей"""

        query = select(func.count(User.guid)).where(User.is_deleted == 0)

        if guids:
            query = query.where(User.guid.in_(guids))

        return (await db.execute(query)).scalar()

    @classmethod
    async def exist_one(cls, db: AsyncSession, guid: UUID4) -> User:
        """Получение существования пользователя"""

        query = select(User.guid).where(User.guid == guid, User.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_one(cls, db: AsyncSession, guid: UUID4) -> User:
        """Получение пользователя по идентификатору"""

        query = select(User).where(User.guid == guid, User.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> User:
        """Получение пользователя по email"""

        query = select(User).where(User.email == email, User.is_deleted == 0)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_multiple(cls, db: AsyncSession, guids: Optional[List[UUID4]], limit: int, offset: int) -> List[User]:
        """Получение пользователей по идентификаторам"""

        query = select(User).where(User.is_deleted == 0)

        if guids is not None:
            query = query.where(User.guid.in_(guids))

        users = (await db.execute(query.limit(limit).offset(cast(offset, BigInteger)))).scalars()
        return users

    @classmethod
    async def create(cls, db: AsyncSession, user_form: UserCreate) -> User:
        """Создание пользователя"""

        user = User(**user_form.to_db_dict())
        db.add(user)
        await db.flush()
        return user

    @classmethod
    async def update(cls, db: AsyncSession, guid: UUID4, user_form: UserCreate) -> User:
        """Полное обновление пользователя"""

        return await cls._change_one(db=db, guid=guid, user_form=user_form)

    @classmethod
    async def patch(cls, db: AsyncSession, guid: UUID4, user_form: UserPatch) -> User:
        """Частичное обновление пользователя"""

        return await cls._change_one(db=db, guid=guid, user_form=user_form)

    @classmethod
    async def delete(cls, db: AsyncSession, guid: UUID4) -> None:
        """Удаление пользователя"""

        query = update(User).where(User.guid == guid).values(is_deleted=1)
        await db.execute(query)

    @classmethod
    async def _change_one(cls, db: AsyncSession, guid: UUID4, user_form: Union[UserCreate, UserPatch]) -> User:
        """Общий метод обновления пользователей"""

        query = update(User).where(User.guid == guid).values(**user_form.dict(exclude_unset=True))
        await db.execute(query)
        await db.flush()

        return await cls.get_one(db=db, guid=guid)
