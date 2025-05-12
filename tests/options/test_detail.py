from uuid import uuid4


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

    def test_remove_duplicate_patch(self, auth_client, option_data, create_option):
        detail_url = self.build_url(create_option.json()["pk"])
        data = {"name": f"Unique-Tier-{uuid4().hex[:8]}"}
        response = auth_client.patch(detail_url, json=data)
        assert response.status_code == 200

        list_url = self.url
        response = auth_client.post(list_url, json=option_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == option_data["name"]
