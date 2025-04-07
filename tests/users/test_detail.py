class TestDetailUsers:
    url = "/users/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get(self, client, user_tokens):
        url = self.build_url(user_tokens["pk"])
        response = client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert "pk" in data and "username" in data
        assert "password" not in data

    def test_invalid_method(self, client, user_tokens):
        new_username = "new-username"
        url = self.build_url(user_tokens["pk"])
        response = client.put(url, data={"username": new_username})
        assert response.status_code == 405

    def test_without_pk(self, auth_client):
        response = auth_client.get(self.url)
        data = response.json()
        assert data == {}
