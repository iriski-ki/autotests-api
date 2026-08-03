from http import HTTPStatus

from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from clients.authentication.authenticationClient import get_authentication_client
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response
from clients.users.public_users_client import get_public_users_client


def test_login():
    # Инициализируем API-клиент для работы с пользователями
    public_users_client = get_public_users_client()
    # Формируем тело запроса на создание пользователя
    request_user = CreateUserRequestSchema()
    # Отправляем запрос на создание пользователя
    response_user = public_users_client.create_user_api(request_user)

    # Инициализируем API-клиент для работы с пользователями
    authentication_client = get_authentication_client()
    # Формируем тело запроса на аунтефикацию пользователя
    request_authentication = LoginRequestSchema(
        email=request_user.email,
        password=request_user.password
    )
    # Отправляем запрос на аунтификацию пользователя
    response_authentication = authentication_client.login_api(request_authentication)
    # Также благодаря встроенной валидации в Pydantic дополнительно убеждаемся, что ответ корректный
    login_response_data = LoginResponseSchema.model_validate_json(response_authentication.text)

    assert_status_code(response_authentication.status_code, HTTPStatus.OK)
    # Используем функцию для проверки ответа аунтификации юзера
    assert_login_response(login_response_data)
    # Проверяем, что тело ответа соответствует ожидаемой JSON-схеме
    validate_json_schema(response_authentication.json(), login_response_data.model_json_schema())
