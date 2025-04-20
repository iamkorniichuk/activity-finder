class TestListVenues:
    url = "/venues/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_successful_post(self, auth_client, venue_data, media_data):
        response = auth_client.post(
            self.url,
            data=venue_data,
            files=media_data,
        )
        assert response.status_code == 201
        data = response.json()
        assert "location" in data

        for image in data["media"]:
            response = auth_client.get(image["file"])
            assert response.status_code == 200

    def test_no_media_files(self, auth_client, venue_data, route_data):
        response = auth_client.post(
            self.url,
            data=venue_data,
            files=route_data,
        )
        assert response.status_code == 400
