from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import config
from app.exceptions import catch_unhandled_exceptions
from app.routers.answer import router as answer_router
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.question import router as question_router
from app.routers.test import router as test_router
from app.routers.user import router as user_router

tags_metadata = [
    {"name": "auth", "description": "Работа с авторизацией"},
    {"name": "user", "description": "Работа с пользователями"},
    {"name": "test", "description": "Работа с тестами"},
    {"name": "question", "description": "Работа с вопросами"},
    {"name": "answer", "description": "Работа с ответами"},
    {"name": "health", "description": "Состояние сервиса"},
]

app = FastAPI(
    debug=config.DEBUG,
    openapi_tags=tags_metadata,
    title=config.BACKEND_TTILE,
    description=config.BACKEND_DESCRIPTION,
)
app.middleware('http')(catch_unhandled_exceptions)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth_router, tags=['auth'])
app.include_router(user_router, tags=['user'])
app.include_router(test_router, tags=['test'])
app.include_router(question_router, tags=['question'])
app.include_router(answer_router, tags=['answer'])
app.include_router(health_router, tags=['health'])
