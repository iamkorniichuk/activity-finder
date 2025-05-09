from copy import copy


class TestListBookings:
    url = "/bookings/"

    def test_invalid_week_day(self, auth_client, booking_data):
        booking_data["week_day"] = 6
        response = auth_client.post(self.url, json=booking_data)
        assert response.status_code == 400

    def test_invalid_time(self, auth_client, booking_data):
        data = copy(booking_data)
        data["time"] = "21:00"
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400

        data = copy(booking_data)
        data["time"] = "13:00"
        response = auth_client.post(self.url, json=data)
        assert response.status_code == 400

    def test_indivisible_interval(self, auth_client, booking_data):
        booking_data["time"] = "08:30"
        response = auth_client.post(self.url, json=booking_data)
        assert response.status_code == 400
