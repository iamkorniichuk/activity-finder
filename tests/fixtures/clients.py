import pytest
import httpx


BASE_URL = "http://proxy/"


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


@pytest.fixture
def client1():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


@pytest.fixture
def auth_client(client, signup_user):
    client.headers["Authorization"] = f"Bearer {signup_user.json()['access']}"
    yield client


@pytest.fixture
def auth_client1(client1, signup_user1):
    client1.headers["Authorization"] = f"Bearer {signup_user1.json()['access']}"
    yield client1
