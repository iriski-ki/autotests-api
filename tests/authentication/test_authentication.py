from http import HTTPStatus
import pytest  # Импортируем библиотеку pytest
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.authentication.authenticationClient import AuthenticationClient
from fixtures.users import UserFixture
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.authentication  # Добавили маркировку users
@pytest.mark.regression  # Добавили маркировку regression
class TestAuthentication:
    def test_login(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        # Формируем тело запроса на аунтефикацию пользователя
        request = LoginRequestSchema(email=function_user.email, password=function_user.password)
        # Отправляем запрос на аунтификацию пользователя
        response = authentication_client.login_api(request)
        # Также благодаря встроенной валидации в Pydantic дополнительно убеждаемся, что ответ корректный
        login_response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        # Используем функцию для проверки ответа аунтификации юзера
        assert_login_response(login_response_data)
        # Проверяем, что тело ответа соответствует ожидаемой JSON-схеме
        validate_json_schema(response.json(), login_response_data.model_json_schema())
