import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_corrections_flow():
    # Initial list might have some, but let's record a new one
    correction_payload = {
        "ocr_text": "Doloo 650",
        "system_guess": "Crocin 500mg",
        "user_correction": "Dolo 650",
        "confidence": 0.45
    }

    # Post correction
    response = client.post("/api/corrections", json=correction_payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "success"
    assert "recorded" in res_data["message"]

    # Get corrections list and check if the inserted one is present
    get_response = client.get("/api/corrections")
    assert get_response.status_code == 200
    corrections_list = get_response.json()
    assert isinstance(corrections_list, list)
    assert len(corrections_list) > 0

    # The most recent correction should match what we posted
    latest = corrections_list[0]
    assert latest["ocr_text"] == "Doloo 650"
    assert latest["system_guess"] == "Crocin 500mg"
    assert latest["user_correction"] == "Dolo 650"
    assert latest["confidence"] == 0.45
