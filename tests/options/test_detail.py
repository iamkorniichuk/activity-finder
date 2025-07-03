class TestDetailOptions:
    url = "/options/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get(self, client, create_option):
        url = self.build_url(create_option.json()["pk"])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
