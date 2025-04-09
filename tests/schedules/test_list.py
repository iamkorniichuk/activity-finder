class TestListSchedules:
    url = "/schedules/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_duplicate_days(self, auth_client):
        data = {
            "work_days": [
                {
                    "day": 0,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
                {
                    "day": 1,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
                {
                    "day": 0,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
            ],
            "booking_duration": "01:00:00",
        }
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400

    def test_invalid_time_range(self, auth_client):
        data = {
            "work_days": [
                {
                    "day": 0,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "14:00", "end": "13:00"}],
                },
                {
                    "day": 1,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
                {
                    "day": 2,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
            ],
            "booking_duration": "01:00:00",
        }
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400

    def test_indivisible_interval(self, auth_client):
        data = {
            "work_days": [
                {
                    "day": 0,
                    "work_hours": {"start": "08:00", "end": "17:30"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
                {
                    "day": 1,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
                {
                    "day": 2,
                    "work_hours": {"start": "08:00", "end": "18:00"},
                    "break_hours": [{"start": "13:00", "end": "14:00"}],
                },
            ],
            "booking_duration": "01:00:00",
        }
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400
