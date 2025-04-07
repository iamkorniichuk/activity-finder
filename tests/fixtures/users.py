import pytest
from uuid import uuid4


@pytest.fixture
def user_data():
    yield {
        "username": f"user-{uuid4().hex[:8]}",
        "password": "StrongP@ssw0rd!",
    }


@pytest.fixture
def user_tokens(signup_user):
    yield signup_user.json()


@pytest.fixture
def signup_user(client, user_data):
    yield client.post("/auth/signup/", json=user_data)


@pytest.fixture
def user_multiple_tokens(client, signup_user, user_data):
    tokens = []
    for _ in range(3):
        response = client.post("/auth/login/", json=user_data)
        tokens.append(response.json())
    yield tokens
