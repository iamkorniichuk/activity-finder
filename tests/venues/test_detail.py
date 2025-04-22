from uuid import uuid4


class TestDetailVenues:
    url = "/venues/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get(self, client, create_venue):
        url = self.build_url(create_venue.json()["pk"])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_successful_patch(self, auth_client, create_venue):
        url = self.build_url(create_venue.json()["pk"])
        data = {"name": "Normal club"}
        response = auth_client.patch(url, data=data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Normal club"

    def test_override_created_by(self, auth_client, create_venue):
        user_data = {
            "username": f"user-{uuid4().hex[:8]}",
            "password": "StrongP@ssw0rd!",
        }
        user_tokens = auth_client.post("/auth/signup/", json=user_data).json()

        url = self.build_url(create_venue.json()["pk"])

        data = {"created_by": user_tokens["pk"]}
        response = auth_client.patch(url, data=data)
        assert response.status_code == 200

        auth_client.headers["Authorization"] = f"Bearer {user_tokens['access']}"
        response = auth_client.patch(url, data=data)
        assert response.status_code == 403
