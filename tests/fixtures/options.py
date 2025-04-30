import pytest
from uuid import uuid4


@pytest.fixture
def option_data(create_recurring_activity):
    yield {
        "name": f"Tier-{uuid4().hex[:8]}",
        "description": "The most basic entrance tier",
        "activity_pk": create_recurring_activity.json()["pk"],
    }


@pytest.fixture
def create_option(auth_client, option_data):
    response = auth_client.post("/options/", json=option_data)
    assert response.status_code == 201
    yield response
