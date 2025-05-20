class TestMyListReactions:
    url = "/reactions/my/"

    def test_successful_get(self, auth_client, auth_client1, create_reaction):
        response = auth_client.get(self.url)
        assert response.status_code == 200
        data = response.json()["results"]
        assert isinstance(data, list)

        response = auth_client1.get(self.url)
        data = response.json()["results"]
        assert isinstance(data, list)
        for obj in data:
            assert data["pk"] != create_reaction.json()["pk"]
