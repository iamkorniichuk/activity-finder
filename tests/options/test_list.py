class TestListOptions:
    url = "/options/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()["results"]
        assert isinstance(data, list)

    def test_foreign_activity_post(self, auth_client1, option_data):
        response = auth_client1.post(self.url, json=option_data)
        assert response.status_code == 400
        data = response.json()
        assert "activity_pk" in data
