import pytest


@pytest.fixture
def schedule_data():
    yield {
        "work_days": [
            {
                "day": 0,
                "work_hours": {"start": "", "end": ""},
                "break_hours": [{"start": "", "end": ""}],
            }
        ],
        "booking_duration": "01:00:00",
    }


@pytest.fixture
def create_schedule(auth_client, schedule_data):
    yield auth_client.post("/schedules/", json=schedule_data)
