class TestLogoutAllAuth:
    url = "/auth/logout-all/"

    def test_require_auth(self, client):
        response = client.post(self.url)
        assert response.status_code == 401

    def test_successful(self, client, user_multiple_tokens):
        tokens = user_multiple_tokens.pop()
        headers = {"Authorization": f"Bearer {tokens['access']}"}
        response = client.post(self.url, headers=headers)
        assert response.status_code == 200

        for data in user_multiple_tokens:
            response = client.post(
                "/auth/login-refresh/", json={"refresh": data["refresh"]}
            )
            assert response.status_code == 401
