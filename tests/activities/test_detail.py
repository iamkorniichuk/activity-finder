class TestDetailActivities:
    url = "/activities/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get_recurring(self, client, publish_recurring_activity):
        url = self.build_url(publish_recurring_activity.json()["pk"])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_hidden_get(self, client1, create_recurring_activity):
        url = self.build_url(create_recurring_activity.json()["pk"])
        response = client1.get(url)
        assert response.status_code == 404

    def test_foreign_get(self, auth_client1, publish_recurring_activity):
        url = self.build_url(publish_recurring_activity.json()["pk"])
        response = auth_client1.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_successful_patch_recurring(self, auth_client, publish_recurring_activity):
        url = self.build_url(publish_recurring_activity.json()["pk"])
        data = {"name": "Super VR game"}
        response = auth_client.patch(url, data=data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Super VR game"

    def test_type_patch(self, auth_client, publish_recurring_activity):
        url = self.build_url(publish_recurring_activity.json()["pk"])
        data = {"name": "Super VR game", "type": "OneTimeActivity"}
        response = auth_client.patch(url, data=data)
        assert response.status_code == 400

    def test_nonexistent_field_patch(self, auth_client, publish_recurring_activity):
        url = self.build_url(publish_recurring_activity.json()["pk"])
        data = {"time_range": "15:00:00-21:00:00"}
        response = auth_client.patch(url, data=data)
        assert "time_range" not in response.json()

    def test_foreign_schedule_patch(
        self, auth_client, auth_client1, schedule_data, publish_recurring_activity
    ):
        foreign_schedule_pk = auth_client1.post(
            "/schedules/", json=schedule_data
        ).json()["pk"]

        url = self.build_url(publish_recurring_activity.json()["pk"])
        response = auth_client.patch(url, data={"schedule_pk": foreign_schedule_pk})
        assert response.status_code == 400
        data = response.json()
        assert "schedule_pk" in data
