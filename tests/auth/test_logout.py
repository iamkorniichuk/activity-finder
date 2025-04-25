class TestLogoutAuth:
    url = "/auth/logout/"

    def test_missing_token(self, client):
        response = client.post(self.url, json={})
        assert response.status_code == 400

    def test_successful(self, client, signup_user):
        refresh_token = signup_user.json()["refresh"]

        data = {"refresh": refresh_token}
        response = client.post(self.url, json=data)
        assert response.status_code == 200

        response = client.post(
            "/auth/login-refresh/",
            json={"refresh": refresh_token},
        )
        assert response.status_code == 401
