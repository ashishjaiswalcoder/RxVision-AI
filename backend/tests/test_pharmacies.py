import pytest
import os
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_pharmacies_mock():
    # If GOOGLE_MAPS_API_KEY environment variable is not set or empty, mock generation is triggered
    if "GOOGLE_MAPS_API_KEY" in os.environ:
        del os.environ["GOOGLE_MAPS_API_KEY"]

    response = client.get("/api/pharmacies?lat=12.971598&lng=77.594562&radius=2000")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for pharmacy in data:
        assert "id" in pharmacy
        assert "name" in pharmacy
        assert "address" in pharmacy
        assert "lat" in pharmacy
        assert "lng" in pharmacy
        assert "rating" in pharmacy
        assert "open_now" in pharmacy
        assert "distance_m" in pharmacy
        assert isinstance(pharmacy["lat"], float)
        assert isinstance(pharmacy["lng"], float)
        assert isinstance(pharmacy["distance_m"], int)

def test_get_pharmacies_google_mocked(monkeypatch):
    # Set the environmental variable to trigger google logic branch
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "fake_key_123")

    # Mocking requests.get to return a simulated google api response
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "results": [
                    {
                        "place_id": "google_place_1",
                        "name": "Google Mocked Pharmacy",
                        "vicinity": "123 Google Road, Near Server",
                        "geometry": {
                            "location": {
                                "lat": 12.971598,
                                "lng": 77.594562
                            }
                        },
                        "rating": 4.5,
                        "opening_hours": {
                            "open_now": True
                        }
                    }
                ]
            }

    import requests
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    response = client.get("/api/pharmacies?lat=12.971598&lng=77.594562&radius=1000")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    pharmacy = data[0]
    assert pharmacy["id"] == "google_place_1"
    assert pharmacy["name"] == "Google Mocked Pharmacy"
    assert pharmacy["address"] == "123 Google Road, Near Server"
    assert pharmacy["lat"] == 12.971598
    assert pharmacy["lng"] == 77.594562
    assert pharmacy["rating"] == 4.5
    assert pharmacy["open_now"] is True

def test_get_pharmacies_missing_parameters():
    response = client.get("/api/pharmacies")
    assert response.status_code == 422 # Unprocessable Entity
