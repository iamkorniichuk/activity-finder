class TestDetailSchedules:
    url = "/schedules/"

    def build_url(self, pk):
        return f"{self.url}{pk}/"

    def test_successful_get(self, client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        correct_slots = [
            "08:00:00",
            "09:00:00",
            "10:00:00",
            "11:00:00",
            "12:00:00",
            "14:00:00",
            "15:00:00",
            "16:00:00",
            "17:30:00",
            "18:30:00",
        ]
        data_slots = data["work_days"][0]["slots"]
        for i in range(len(correct_slots)):
            assert data_slots[i]["time"] == correct_slots[i]

    def test_successful_duration_patch(self, auth_client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        data = {"booking_duration": "00:30:00"}
        response = auth_client.patch(url, json=data)
        assert response.status_code == 200
        data = response.json()
        assert data["booking_duration"] == data["booking_duration"]
        correct_slots = [
            "08:00:00",
            "08:30:00",
            "09:00:00",
            "09:30:00",
            "10:00:00",
            "10:30:00",
            "11:00:00",
            "11:30:00",
            "12:00:00",
            "12:30:00",
            "14:00:00",
            "14:30:00",
            "15:00:00",
            "15:30:00",
            "16:00:00",
            "16:30:00",
            "17:30:00",
            "18:00:00",
            "18:30:00",
            "19:00:00",
        ]
        data_slots = data["work_days"][0]["slots"]
        for i in range(len(correct_slots)):
            assert data_slots[i]["time"] == correct_slots[i]

    def test_successful_work_days_patch(self, auth_client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        data = {
            "work_days": [
                {
                    "week_day": 0,
                    "work_hours": "08:00-18:00",
                    "break_hours": ["13:00:00-14:00:00"],
                },
                {
                    "week_day": 1,
                    "work_hours": "08:00-18:00",
                },
            ]
        }
        response = auth_client.patch(url, json=data)
        assert response.status_code == 200
        data = response.json()
        correct_slots = [
            "08:00:00",
            "09:00:00",
            "10:00:00",
            "11:00:00",
            "12:00:00",
            "14:00:00",
            "15:00:00",
            "16:00:00",
            "17:00:00",
        ]
        data_slots = data["work_days"][0]["slots"]
        for i in range(len(correct_slots)):
            assert data_slots[i]["time"] == correct_slots[i]

    def test_indivisible_interval(self, auth_client, create_schedule):
        url = self.build_url(create_schedule.json()["pk"])
        data = {"booking_duration": "00:55:00"}
        response = auth_client.patch(url, json=data)
        assert response.status_code == 400
