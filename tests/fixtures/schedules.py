import pytest


@pytest.fixture
def schedule_data():
    yield {
        "work_days": [
            {
                "day": 0,
                "work_hours": "08:00-19:30",
                "break_hours": ["13:00:00-14:00:00", "17:00:00-17:30:00"],
            },
            {
                "day": 1,
                "work_hours": "08:00-18:00",
                "break_hours": ["13:00:00-14:00:00"],
            },
            {
                "day": 2,
                "work_hours": "08:00-18:00",
                "break_hours": ["13:00:00-14:00:00"],
            },
            {
                "day": 3,
                "work_hours": "08:00:00-18:00:00",
                "break_hours": ["13:00:00-14:00:00"],
            },
            {
                "day": 4,
                "work_hours": "08:00:00-18:00:00",
            },
        ],
        "booking_duration": "01:00:00",
    }


@pytest.fixture
def create_schedule(auth_client, schedule_data):
    yield auth_client.post("/schedules/", json=schedule_data)
