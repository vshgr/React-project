from datetime import datetime, timedelta
from typing import Dict, Union
from uuid import uuid4

from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.models import Token
from app.models.user import UserCreate, UserGet
from app.services.api.user import UserService
from app.services.db.user import UserDBService


class AuthService:
    @classmethod
    async def login(cls, db: AsyncSession, token: str) -> Token:
        """Авторизация пользователя через Google Oauth2"""

        logger.debug(f"Запрос на авторизацию пользователя: {token =}")

        user = cls._authorize_user(token)
        logger.debug(f"Пользователь авторизован: {user}")

        user_db = await UserDBService.get_by_email(db=db, email=user["email"])

        if not user_db:
            user_form = UserCreate(email=user["email"], name=user["given_name"], surname=user["family_name"])
            new_user = await UserService.create_user(db=db, user_form=user_form)
        else:
            new_user = UserGet.from_orm(user_db)

        payload = cls._get_payload(new_user)
        access_token = cls._create_access_token(payload)

        return Token(access_token=access_token)

    @classmethod
    def _authorize_user(cls, token: str) -> dict:
        try:
            return id_token.verify_oauth2_token(token, requests.Request(), config.GOOGLE_CLIENT_ID)
        except ValueError:
            raise HTTPException(401, "Ошибка авторизации")

    @classmethod
    def _get_payload(cls, user: UserGet) -> Dict[str, Union[datetime, str]]:
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(minutes=config.BACKEND_JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "exp": expires_at,
            "iat": created_at,
            "jti": str(uuid4()),
            "sub": str(user.guid),
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
        }

    @classmethod
    def _create_access_token(cls, payload: Dict[str, Union[datetime, str]]) -> str:
        return jwt.encode(
            payload,
            config.BACKEND_JWT_SECRET,
            algorithm=config.BACKEND_JWT_ALGORITHM,
        )
