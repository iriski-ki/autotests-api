from http import HTTPStatus

import allure
import pytest  # Импортируем библиотеку pytest
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.authentication.authenticationClient import AuthenticationClient
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.authentication  # Добавили маркировку users
@pytest.mark.regression  # Добавили маркировку regression
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.AUTHENTICATION)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.AUTHENTICATION)
class TestAuthentication:
    @allure.tag(AllureTag.AUTHENTICATION)
    @allure.sub_suite(AllureSubSuite.LOGIN)
    @allure.title("Authorization Test")
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
