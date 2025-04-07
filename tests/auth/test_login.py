import pytest


class TestLoginAuth:
    url = "/auth/login/"

    def test_successful(self, client, signup_user, user_data):
        response = client.post(self.url, json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert "access" in data and "refresh" in data

    @pytest.mark.parametrize(
        "password",
        [
            "WrongP@ssw0rd!",
            "StrongP@ssw0rd",
            "strongp@ssw0rd!",
        ],
    )
    def test_wrong_password(self, client, signup_user, user_data, password):
        user_data["password"] = password
        response = client.post(self.url, json=user_data)
        assert response.status_code == 401

    def test_nonexistent_user(self, client, user_data):
        response = client.post(self.url, json=user_data)
        assert response.status_code == 401

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
