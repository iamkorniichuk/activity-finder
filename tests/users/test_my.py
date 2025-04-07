from uuid import uuid4


class TestMyObjectUsers:
    url = "/users/my/"

    def test_successful_get(self, auth_client, user_data):
        response = auth_client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert "username" in data and "image" in data
        assert data["username"] == user_data["username"]

    def test_successful_put(self, auth_client):
        new_username = f"user-{uuid4().hex[:6]}"
        response = auth_client.put(self.url, data={"username": new_username})
        assert response.status_code == 200
        data = response.json()
        assert "username" in data
        assert data["username"] == new_username

    def test_successful_patch(self, auth_client):
        new_description = "New description"
        response = auth_client.patch(self.url, data={"description": new_description})
        assert response.status_code == 200
        data = response.json()
        assert "username" in data and "description" in data
        assert data["description"] == new_description

    def test_invalid_method(self, auth_client):
        response = auth_client.delete(self.url)
        assert response.status_code == 405

    def test_require_auth(self, client):
        response = client.get(self.url)
        assert response.status_code == 401
