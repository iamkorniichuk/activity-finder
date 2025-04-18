import pytest


@pytest.fixture
def media_data():
    image1 = open("./fixtures/media/image1.png", "rb")
    image2 = open("./fixtures/media/image2.jpg", "rb")
    video1 = open("./fixtures/media/video1.mp4", "rb")

    yield {
        "media[0]": image1,
        "media[1]": image2,
        "media[2]": video1,
    }

    image1.close()
    image2.close()
    video1.close()


@pytest.fixture
def recurring_activity_data(create_schedule):
    yield {
        "name": "VR games",
        "description": "Play VR games with your friends!",
        "type": "RecurringActivity",
        "location": "",
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
def one_time_activity_data():
    yield {
        "name": "Music Concert",
        "type": "OneTimeActivity",
        "description": "Listen to your favorite music in live!",
        "date": "2025-06-11",
        "time_range": "12:00:00-19:00:00",
        "location": "-2.378851,-121.443992",
        "is_remote": False,
    }


@pytest.fixture
def create_one_time_activity(auth_client, one_time_activity_data, media_data):
    yield auth_client.post(
        "/activities/",
        data=one_time_activity_data,
        files=media_data,
    )
