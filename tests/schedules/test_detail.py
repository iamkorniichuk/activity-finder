class TestDetailSchedules:
    url = "/schedules/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get(self, client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_successful_duration_patch(self, auth_client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        data = {"booking_duration": "00:30:00"}
        response = auth_client.patch(url, json=data)
        assert response.status_code == 200
        assert response.json()["booking_duration"] == data["booking_duration"]

    def test_successful_work_days_patch(self, auth_client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        data = {
            "work_days": [
                {
                    "day": 0,
                    "work_hours": "08:00-18:00",
                    "break_hours": ["13:00:00-14:00:00"],
                },
                {
                    "day": 1,
                    "work_hours": "08:00-18:00",
                },
            ]
        }
        response = auth_client.patch(url, json=data)
        assert response.status_code == 200

    def test_indivisible_interval(self, auth_client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        data = {"booking_duration": "00:55:00"}
        response = auth_client.patch(url, json=data)
        assert response.status_code == 400
