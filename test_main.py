from fastapi.testclient import TestClient

from main import app

from constants import TEST_LATITUDE
from constants import TEST_LONGITUDE
from constants import TEST_INVALID_LATITUDE
from constants import TEST_INVALID_LONGITUDE


client = TestClient(app)


def test_nasapower_request():
    response = client.get("/", params={
        "latitude": TEST_LATITUDE,
        "longitude": TEST_LONGITUDE
    })

    assert response.status_code == 200


def test_request_without_params():
    response = client.get("/")

    assert response.status_code == 422


def test_request_invalid_coordinates():
    response = client.get("/", params={
        "latitude": TEST_INVALID_LATITUDE,
        "longitude": TEST_INVALID_LONGITUDE
    })

    assert response.status_code == 406
