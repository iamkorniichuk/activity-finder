import pytest


@pytest.fixture
def layout_data(create_venue):
    yield {
        "name": "Main stage",
        "size": "2160,1080",
        "venue_pk": create_venue.json()["pk"],
        "visual_objects": [
            {
                "name": "Stage",
                "position": "2000.50,820.80",
                "size": "100,200",
                "rotation": 0,
                "type": "VisualObject",
            },
            {
                "name": "Director seat",
                "position": "1000, 400",
                "size": "20, 20",
                "rotation": -80,
                "type": "Seat",
            },
            {
                "name": "Regular seat",
                "position": "1500, 300",
                "size": "300, 400",
                "rotation": -45,
                "seat_amount": 40,
                "type": "SeatZone",
            },
        ],
    }


@pytest.fixture
def create_layout(auth_client, layout_data):
    response = auth_client.post("/layouts/", json=layout_data)
    assert response.status_code == 201
    yield response
