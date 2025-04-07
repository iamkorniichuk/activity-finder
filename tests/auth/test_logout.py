class TestLogoutAuth:
    url = "/auth/logout/"

    def test_missing_token(self, client):
        response = client.post(self.url, json={})
        assert response.status_code == 400

    def test_successful(self, client, user_tokens):
        data = {"refresh": user_tokens["refresh"]}
        response = client.post(self.url, json=data)
        assert response.status_code == 200

        response = client.post(
            "/auth/login-refresh/",
            json={"refresh": user_tokens["refresh"]},
        )
        assert response.status_code == 401
