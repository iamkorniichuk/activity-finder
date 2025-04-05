import pytest
import httpx
from uuid import uuid4


BASE_URL = "http://proxy/"


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


@pytest.fixture
def user_data():
    return {
        "username": f"user-{uuid4().hex[:8]}",
        "password": "StrongP@ssw0rd!",
    }


@pytest.fixture
def user(client, user_data):
    client.post("/auth/signup/", json=user_data)
    return user_data


@pytest.fixture
def user_tokens(client, user):
    response = client.post("/auth/login/", json=user)
    return response.json()


@pytest.fixture
def multiple_user_tokens(client, user):
    tokens = []
    for _ in range(3):
        response = client.post("/auth/login/", json=user)
        tokens.append(response.json())
    return tokens
