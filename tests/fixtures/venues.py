import pytest


@pytest.fixture
def venue_data():
    yield {
        "name": "Big Club",
        "description": "The biggest club in your city!",
        "location": "-23.54321,5.54322",
    }


@pytest.fixture
def create_venue(auth_client, venue_data, media_data, route_data):
    files = media_data | route_data
    response = auth_client.post(
        "/venues/",
        data=venue_data,
        files=files,
    )
    assert response.status_code == 201
    yield response


@pytest.fixture
def publish_venue(auth_client, create_venue, create_layout):
    url = f"/venues/{create_venue.json()['pk']}/publish/"
    response = auth_client.post(url)
    assert response.status_code == 200
    yield response
