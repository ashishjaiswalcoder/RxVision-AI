import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "RxVision AI is running!" in data["message"]
    assert "version" in data
    assert "endpoints" in data
    assert data["endpoints"]["upload"] == "/api/upload"
