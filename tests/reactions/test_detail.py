class TestDetailReactions:
    url = "/reactions/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_delete(self, auth_client, create_reaction):
        url = self.build_url(create_reaction.json()["pk"])
        response = auth_client.delete(url)
        assert response.status_code == 204

    def test_foreign_delete(self, auth_client1, create_reaction):
        url = self.build_url(create_reaction.json()["pk"])
        response = auth_client1.delete(url)
        assert response.status_code == 403
