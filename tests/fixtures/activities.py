import pytest


@pytest.fixture
def recurring_activity_data(create_schedule, publish_venue):
    yield {
        "name": "VR games",
        "description": "Play VR games with your friends!",
        "type": "RecurringActivity",
        "duration": "01:00:00",
        "schedule_pk": create_schedule.json()["pk"],
        "venue_pk": publish_venue.json()["pk"],
    }


@pytest.fixture
def create_recurring_activity(auth_client, recurring_activity_data, media_data):
    response = auth_client.post(
        "/activities/",
        data=recurring_activity_data,
        files=media_data,
    )
    assert response.status_code == 201
    yield response


@pytest.fixture
def publish_recurring_activity(auth_client, create_recurring_activity, create_option):
    url = f"/activities/{create_recurring_activity.json()['pk']}/publish/"
    response = auth_client.post(url)
    assert response.status_code == 200
    yield response


@pytest.fixture
def one_time_activity_data(publish_venue, create_layout):
    yield {
        "name": "Music Concert",
        "type": "OneTimeActivity",
        "description": "Listen to your favorite music in live!",
        "date": "2025-06-11",
        "time_range": "12:00:00-19:00:00",
        "venue_pk": publish_venue.json()["pk"],
        "layout_pk": create_layout.json()["pk"],
    }


@pytest.fixture
def create_one_time_activity(auth_client, one_time_activity_data, media_data):
    response = auth_client.post(
        "/activities/",
        data=one_time_activity_data,
        files=media_data,
    )
    assert response.status_code == 201
    yield response


@pytest.fixture
def publish_one_time_activity(auth_client, create_one_time_activity):
    url = f"/activities/{create_one_time_activity.json()['pk']}/publish/"
    response = auth_client.post(url)
    assert response.status_code == 200
    yield response
