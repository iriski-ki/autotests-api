from http import HTTPStatus

from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
# Импортируем функцию для проверки ответа создания юзера
from tools.assertions.users import assert_create_user_response
import pytest

from tools.fakers import fake


@pytest.mark.parametrize("email", ["mail.ru",
                                   "gmail.com",
                                   "example.com"
                                   ], )
@pytest.mark.users
@pytest.mark.regression
def test_create_user(email: str,public_users_client:PublicUsersClient):
    custom_email = fake.email(domain=email)
    print(custom_email)
    request = CreateUserRequestSchema(email=custom_email
    )
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    # Используем функцию для проверки ответа создания юзера
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())