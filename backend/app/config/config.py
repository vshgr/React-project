from __future__ import annotations

from functools import lru_cache

from dotenv import find_dotenv
from pydantic import BaseSettings


class _Settings(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Config(_Settings):
    # Debug
    DEBUG: bool

    # Backend
    BACKEND_TTILE: str
    BACKEND_DESCRIPTION: str
    BACKEND_PREFIX: str

    BACKEND_HOST: str
    BACKEND_PORT: int
    BACKEND_RELOAD: bool

    BACKEND_JWT_SECRET: str
    BACKEND_JWT_ALGORITHM: str
    BACKEND_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Google OAuth2
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # PostgreSQL
    POSTGRES_URL: str


@lru_cache()
def get_config(env_file: str = ".env") -> Config:
    return Config(_env_file=find_dotenv(env_file))
