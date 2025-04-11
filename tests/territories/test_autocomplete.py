class TestMyListSchedules:
    url = "/territories/autocomplete/"

    def test_successful_get(self, client):
        response = client.get(self.url, params={"name": "random"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_invalid_params(self, client):
        response = client.get(self.url, params={"query": "random"})
        assert response.status_code == 400
