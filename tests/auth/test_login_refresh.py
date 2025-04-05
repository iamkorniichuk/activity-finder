class TestLoginRefresh:
    url = "/auth/login-refresh/"

    def test_successful(self, client, user_tokens):
        response = client.post(self.url, json={"refresh": user_tokens["refresh"]})
        assert response.status_code == 200
        data = response.json()
        assert "access" in data

    def test_invalid_token(self, client):
        response = client.post(self.url, json={"refresh": "invalidtoken"})
        assert response.status_code == 401

    def test_missing_token(self, client):
        response = client.post(self.url, json={})
        assert response.status_code == 400
