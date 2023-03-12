from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JOSEError, jwt
from pydantic import UUID4

from app.config import config

bearer_scheme = HTTPBearer()


def verify_access_token(access_token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        jwt.decode(
            access_token.credentials,
            config.BACKEND_JWT_SECRET,
            algorithms=[config.BACKEND_JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    except JOSEError:
        raise HTTPException(401, "Неверный токен авторизации", headers={"WWW-Authenticate": "Bearer"})


def get_user_from_access_token(request: Request) -> UUID4:
    access_token = request.headers["Authorization"].split()[1]
    info = jwt.decode(
        access_token,
        config.BACKEND_JWT_SECRET,
        algorithms=[config.BACKEND_JWT_ALGORITHM],
        options={"verify_aud": False},
    )
    return info["sub"]
