from copy import copy


class TestListSchedules:
    url = "/schedules/"

    def test_successful_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_overwrite_created_by(self, auth_client, signup_user, schedule_data: dict):
        data = schedule_data.copy()
        data["created_by"] = 5
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 201
        data = response.json()
        assert data["created_by"]["pk"] == signup_user.json()["pk"]

        data = schedule_data.copy()
        data["created_by_pk"] = 5
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 201
        data = response.json()
        assert data["created_by"]["pk"] == signup_user.json()["pk"]

    def test_duplicate_days(self, auth_client, schedule_data):
        schedule_data["work_days"][0]["week_day"] = 0
        schedule_data["work_days"][1]["week_day"] = 0
        response = auth_client.post(self.url, json=schedule_data)
        assert response.status_code == 400

    def test_invalid_time_range(self, auth_client, schedule_data):
        schedule_data["work_days"][0]["work_hours"] = "00:16:00-00:12:00"
        response = auth_client.post(self.url, json=schedule_data)
        assert response.status_code == 400

    def test_indivisible_interval(self, auth_client, schedule_data):
        data = copy(schedule_data)
        data["work_days"][0]["work_hours"] = "00:08:00-00:17:30"
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400

        data = copy(schedule_data)
        data["work_days"][4]["work_hours"] = "16:00:00-17:30:00"
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400
