class TestMyListSchedules:
    url = "/schedules/my/"

    def test_successful_get(self, auth_client):
        response = auth_client.get(self.url)
        assert response.status_code == 200
        data = response.json()["results"]
        assert isinstance(data, list)

    def test_invalid_method(self, auth_client):
        response = auth_client.post(self.url)
        assert response.status_code == 405

    def test_require_auth(self, client):
        response = client.get(self.url)
        assert response.status_code == 401
