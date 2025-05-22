class TestDetailVenues:
    url = "/venues/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get(self, client, publish_venue):
        url = self.build_url(publish_venue.json()["pk"])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_hidden_get(self, client1, create_venue):
        url = self.build_url(create_venue.json()["pk"])
        response = client1.get(url)
        assert response.status_code == 404

    def test_foreign_get(self, auth_client1, publish_venue):
        url = self.build_url(publish_venue.json()["pk"])
        response = auth_client1.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_successful_patch(self, auth_client, publish_venue):
        url = self.build_url(publish_venue.json()["pk"])
        data = {"name": "Normal club"}
        response = auth_client.patch(url, data=data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Normal club"

    def test_override_created_by(
        self,
        auth_client,
        auth_client1,
        signup_user1,
        publish_venue,
    ):
        url = self.build_url(publish_venue.json()["pk"])

        data = {"created_by": signup_user1.json()["pk"]}
        response = auth_client.patch(url, data=data)
        assert response.status_code == 200

        response = auth_client1.patch(url, data=data)
        assert response.status_code == 403
