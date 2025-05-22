import pytest


@pytest.fixture
def reaction_data(publish_recurring_activity):
    yield {
        "activity_pk": publish_recurring_activity.json()["pk"],
        "type": "like",
    }


@pytest.fixture
def create_reaction(auth_client, reaction_data):
    response = auth_client.post("/reactions/", json=reaction_data)
    assert response.status_code == 201
    yield response
