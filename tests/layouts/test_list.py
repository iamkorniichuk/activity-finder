from copy import copy


class TestListLayouts:
    url = "/layouts/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()["results"]
        assert isinstance(data, list)

    def test_exceed_limits(self, auth_client, layout_data):
        data = copy(layout_data)
        data["size"] = "3000, 50"
        response = auth_client.post("/layouts/", json=data)
        assert response.status_code == 400
        data = response.json()
        assert "size" in data

        data = copy(layout_data)
        data["size"] = "2000, 300, 700"
        response = auth_client.post("/layouts/", json=data)
        assert response.status_code == 400
        data = response.json()
        assert "size" in data
