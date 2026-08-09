import pytest
#Автоматически отправляет аналитику,можно генерировать на класс или на фикстуру через scope
@pytest.fixture(autouse=True)
def send_analytics_data():
    print("[AUTOUSE] Отправляем данные в сервис аналитике")

@pytest.fixture(scope="session")
def setting():
    print("[SESSION] Инициализируем настройки для автотестов")

@pytest.fixture(scope="class")
def user():
    print("[CLASS] Создаем данные пользователя один раз на один тестовый класс")

@pytest.fixture(scope="function")
def user_client():
    print("[FUNCTION] Создание API клиент на новый автотест")

class TestUserFlow:
    def test_user_can_login(self,user, setting,user_client):
        ...
    def test_user_can_create_course(self,setting,user, user_client):
        ...


class TestAccountFlow:
    def test_user_account(self,setting,user, user_client):
        ...

@pytest.fixture
def user_data() ->dict:
    print("Создаем пользователя до теста(setup)")#до теста
    yield {"username": "test", "password": "111111", "email": "sfgsdf@gmail.com"} #сам тест
    print("Удаляем пользователя после теста(teardown)")#после теста

def test_2user(user_data: dict):
    print(user_data)
    assert user_data["username"] == "test"

def test_2user_can(user_data: dict):
    print(user_data)
    assert user_data["email"] == "sfgsdf@gmail.com"