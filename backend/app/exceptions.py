import traceback
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from loguru import logger
from pydantic import UUID4, BaseModel
from starlette.responses import JSONResponse

from app.config import config


async def catch_unhandled_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        error = {
            "message": get_endpoint_message(request),
            "errors": [Message(message='Отказано в обработке из-за неизвестной ошибки на сервере')],
        }
        if not config.DEBUG:
            logger.info(traceback.format_exc())
            return JSONResponse(status_code=500, content=jsonable_encoder(error))
        else:
            raise


class Message(BaseModel):
    id: Optional[UUID4]
    message: str

    def __hash__(self):
        return hash((self.id, self.message))


endpoint_message = {
    ('GET', '/auth'): 'Ошибка работы с авторизацией',
    ("POST", "/user"): "Ошибка создания пользователя",
    ("GET", "/user"): "Ошибка получения списка пользователей",
    ("GET", "/user/{id}"): "Ошибка получения пользователя по идентификатору",
    ("PUT", "/user/{id}"): "Ошибка полного изменения пользователя по идентификатору",
    ("PATCH", "/user/{id}"): "Ошибка частичного изменения пользователя по идентификатору",
    ("DELETE", "/user/{id}"): "Ошибка удаления пользователя по идентификатору",
    ("POST", "/test"): "Ошибка создания теста",
    ("GET", "/test"): "Ошибка получения списка тестов",
    ("GET", "/test/{id}"): "Ошибка получения теста по идентификатору",
    ("PUT", "/test/{id}"): "Ошибка полного изменения теста по идентификатору",
    ("PATCH", "/test/{id}"): "Ошибка частичного изменения теста по идентификатору",
    ("DELETE", "/test/{id}"): "Ошибка удаления теста по идентификатору",
    ("POST", "/question"): "Ошибка создания вопроса",
    ("GET", "/question"): "Ошибка получения списка вопросов",
    ("GET", "/question/{id}"): "Ошибка получения вопроса по идентификатору",
    ("PUT", "/question/{id}"): "Ошибка полного изменения вопроса по идентификатору",
    ("PATCH", "/question/{id}"): "Ошибка частичного изменения вопроса по идентификатору",
    ("DELETE", "/question/{id}"): "Ошибка удаления вопроса по идентификатору",
    ("POST", "/answer"): "Ошибка создания ответа",
    ("GET", "/answer"): "Ошибка получения списка ответов",
    ("GET", "/answer/{id}"): "Ошибка получения ответа по идентификатору",
    ("PUT", "/answer/{id}"): "Ошибка полного изменения ответа по идентификатору",
    ("PATCH", "/answer/{id}"): "Ошибка частичного изменения ответа по идентификатору",
    ("DELETE", "/answer/{id}"): "Ошибка удаления ответа по идентификатору",
    ('GET', '/health'): 'Ошибка проверки состояния сервиса',
    ('HEAD', '/health'): 'Ошибка проверки состояния сервиса',
}


def get_endpoint_message(request: Request):
    method, path = request.scope['method'], request.scope['path']
    for path_parameter, value in request.scope['path_params'].items():
        path = path.replace(value, '{' + path_parameter + '}')
    return endpoint_message.get((method, path))


async def validation_handler(request: Request, exc):
    errors = []
    for error in exc.errors():
        field = error['loc'][1]
        if type(field) == str:
            errors.append(Message(message=f'Поле {field} имеет некорректное значение ({error["type"]})'))
        else:
            errors.append(Message(message=f'Тело запроса содержит некорректные значения ({error["type"]})'))
    error = {"message": get_endpoint_message(request), "errors": list(set(errors))}
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error))


async def logging_handler(request: Request, exc: HTTPException):
    error = {"message": get_endpoint_message(request), "errors": [exc.detail]}
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(error))


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(HTTPException, logging_handler)
