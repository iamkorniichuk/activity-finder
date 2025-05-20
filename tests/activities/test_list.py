class TestListActivities:
    url = "/activities/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()["results"]
        assert isinstance(data, list)

    def test_successful_recurring_post(
        self,
        auth_client,
        recurring_activity_data,
        media_data,
    ):
        response = auth_client.post(
            self.url,
            data=recurring_activity_data,
            files=media_data,
        )
        assert response.status_code == 201
        data = response.json()
        assert "schedule" in data
        assert data["type"] == "RecurringActivity"

    def test_successful_one_time_post(
        self,
        auth_client,
        one_time_activity_data,
        media_data,
    ):
        response = auth_client.post(
            self.url,
            data=one_time_activity_data,
            files=media_data,
        )
        assert response.status_code == 201
        data = response.json()
        assert "time_range" in data
        assert data["type"] == "OneTimeActivity"

    def test_invalid_type(self, auth_client, recurring_activity_data, media_data):
        recurring_activity_data["type"] = "OneTimeActivity"
        response = auth_client.post(
            self.url,
            data=recurring_activity_data,
            files=media_data,
        )
        assert response.status_code == 400

    def test_invalid_files(
        self, auth_client, recurring_activity_data, invalid_media_data
    ):
        response = auth_client.post(
            self.url,
            data=recurring_activity_data,
            files=invalid_media_data,
        )
        assert response.status_code == 400
        data = response.json()
        assert "0" in data["media_files"] and "1" in data["media_files"]

    def test_foreign_schedule_post(
        self,
        auth_client1,
        recurring_activity_data,
        media_data,
    ):
        response = auth_client1.post(
            self.url,
            data=recurring_activity_data,
            files=media_data,
        )
        assert response.status_code == 400
        data = response.json()
        assert "schedule_pk" in data
