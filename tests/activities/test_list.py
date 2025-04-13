class TestListActivities:
    url = "/activities/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_successful_recurring_post(
        self,
        auth_client,
        recurring_activity_data,
        files_data,
    ):
        response = auth_client.post(
            self.url,
            data=recurring_activity_data,
            files=files_data,
        )
        assert response.status_code == 201
        data = response.json()
        assert "schedule" in data
        assert data["type"] == "RecurringActivity"

    def test_successful_one_time_post(
        self,
        auth_client,
        one_time_activity_data,
        files_data,
    ):
        response = auth_client.post(
            self.url,
            data=one_time_activity_data,
            files=files_data,
        )
        assert response.status_code == 201
        data = response.json()
        assert "time_range" in data
        assert data["type"] == "OneTimeActivity"

    def test_invalid_type(self, auth_client, recurring_activity_data, files_data):
        recurring_activity_data["type"] = "OneTimeActivity"
        response = auth_client.post(
            self.url,
            data=recurring_activity_data,
            files=files_data,
        )
        assert response.status_code == 400
