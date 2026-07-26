from jsonschema import validate

from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import get_private_users_client
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, GetUserResponseSchema
from tools.fakers import fake
from tools.assertions.schema import validate_json_schema

# 1. Создаем пользователя через публичный клиент (без авторизации)
public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_response = public_users_client.create_user(create_user_request)

# 2. Авторизуемся под только что созданным пользователем
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
private_users_client = get_private_users_client(authentication_user)

# 3. Получаем данные о созданном пользователе
get_user_response = private_users_client.get_user_api(create_user_response.user.id)
get_user_response_data = get_user_response.json()

# 4. Генерируем JSON schema на основе модели GetUserResponseSchema
get_user_response_schema = GetUserResponseSchema.model_json_schema()

# 5. Валидируем ответ по сгенерированной JSON schema
validate_json_schema(instance=get_user_response_data, schema=get_user_response_schema)

print("JSON schema валидна для ответа GET /api/v1/users/{user_id}")