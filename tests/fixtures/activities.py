import pytest


@pytest.fixture
def recurring_activity_data(create_schedule):
    yield {
        "name": "VR games",
        "description": "Play VR games with your friends!",
        "type": "RecurringActivity",
        "duration": "01:00:00",
        "is_remote": True,
        "schedule_pk": create_schedule.json()["pk"],
    }


@pytest.fixture
def create_recurring_activity(auth_client, recurring_activity_data, media_data):
    yield auth_client.post(
        "/activities/",
        data=recurring_activity_data,
        files=media_data,
    )


@pytest.fixture
def one_time_activity_data(create_venue):
    yield {
        "name": "Music Concert",
        "type": "OneTimeActivity",
        "description": "Listen to your favorite music in live!",
        "date": "2025-06-11",
        "time_range": "12:00:00-19:00:00",
        "venue_pk": create_venue.json()["pk"],
        "is_remote": False,
    }


@pytest.fixture
def create_one_time_activity(auth_client, one_time_activity_data, media_data):
    yield auth_client.post(
        "/activities/",
        data=one_time_activity_data,
        files=media_data,
    )
