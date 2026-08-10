import pytest

from clients.authentication.authenticationClient import AuthenticationClient, get_authentication_client


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()