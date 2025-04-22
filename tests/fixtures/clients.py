import pytest
import httpx


BASE_URL = "http://proxy/"


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


@pytest.fixture
def auth_client(client, user_tokens):
    client.headers["Authorization"] = f"Bearer {user_tokens['access']}"
    yield client
