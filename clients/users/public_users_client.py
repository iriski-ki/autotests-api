from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class CreateUserRequestDict(TypedDict):
    """
    Структура данных для запроса на создание пользователя.

    Описывает тело запроса (payload), отправляемое на эндпоинт
    POST /api/v1/users.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичными методами API пользователей
    (/api/v1/users), не требующими авторизации.
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Выполняет POST-запрос на создание нового пользователя.

        :param request: Данные пользователя для создания
            (email, password, lastName, firstName, middleName).
        :return: Объект httpx.Response с данными ответа сервера,
            включая созданного пользователя в теле ответа.
        """
        return self.post("/api/v1/users", json=request)