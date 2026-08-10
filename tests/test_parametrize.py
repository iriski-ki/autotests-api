import pytest

from clients.authentication.authentication_schema import LoginRequestSchema


@pytest.mark.parametrize("username,password", [
    ("john", "1234"),
    ("john", ""),
    ("john", ""),
])
def login_req(username, password):
    assert login(username, password) == "Success"


@pytest.mark.parametrize("number", [
                         pytest.param(1),
                         pytest.param(2),
                         pytest.param(3),
                         pytest.param(4, marks=pytest.mark.skip(reason="Negative value")),

])
def test_number(number):
    assert number>0


@pytest.mark.parametrize("host", ["localhost", "example.com"])
@pytest.mark.parametrize("port", [1000, 2000, 3000])
def test_host(host, port):
    full_address = f"{host}:{port}"
    assert isinstance(full_address, str)


@pytest.mark.parametrize("number", [1, 2, 3, -1])
def test_number(number: int):


    assert number > 0


@pytest.mark.parametrize("number, expected", [(1, 1), (2, 4), (3, 9)]
)
def test_number(number: int, expected: int):
    assert number ** 2 == expected