import pytest


@pytest.fixture
def booking_data(create_option):
    yield {
        "option_pk": create_option.json()["pk"],
        "week_day": 1,
        "time": "09:00:00",
    }


@pytest.fixture
def create_booking(auth_client, booking_data):
    response = auth_client.post("/bookings/", json=booking_data)
    assert response.status_code == 201
    yield response
