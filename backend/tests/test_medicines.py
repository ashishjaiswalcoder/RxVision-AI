import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_all_medicines, search_medicines

client = TestClient(app)

def test_list_medicines_all():
    response = client.get("/api/medicines")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check details of first medicine
    first_med = data[0]
    assert "medicine_name" in first_med
    assert "generic_name" in first_med
    assert "company_name" in first_med
    assert "dosage_form" in first_med

def test_list_medicines_search():
    # Search for Dolo which exists in standard seed
    response = client.get("/api/medicines?q=Dolo")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Every returned medicine should match the query or its generic name or aliases
    for med in data:
        assert (
            "dolo" in med["medicine_name"].lower() or
            "dolo" in med["generic_name"].lower() or
            "dolo" in med["aliases"].lower()
        )

def test_list_medicines_search_empty():
    response = client.get("/api/medicines?q=NonExistentMedicineName")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
