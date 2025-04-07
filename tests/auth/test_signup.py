import pytest
from uuid import uuid4


class TestSignUpAuth:
    url = "/auth/signup/"

    def test_successful(self, client, user_data):
        response = client.post(self.url, json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert "access" in data and "refresh" in data

    @pytest.mark.parametrize(
        "username,password",
        [
            ("", "StrongP@ssw0rd!"),
            ("user", ""),
            ("", ""),
        ],
    )
    def test_missing_fields(self, client, username, password):
        response = client.post(
            self.url,
            json={"username": username, "password": password},
        )
        assert response.status_code == 400
        data = response.json()
        assert "access" not in data and "refresh" not in data

    @pytest.mark.parametrize(
        "password",
        [
            "123",
            "pass",
            "password",
            "abc123",
        ],
    )
    def test_weak_password(self, client, password):
        user = {"username": f"user-{uuid4().hex[:6]}", "password": password}
        response = client.post(self.url, json=user)
        assert response.status_code == 400
        data = response.json()
        assert "password" in data

    def test_duplicate_user(self, client, signup_user, user_data):
        response = client.post(self.url, json=user_data)
        assert response.status_code == 400
        data = response.json()
        assert "username" in data
