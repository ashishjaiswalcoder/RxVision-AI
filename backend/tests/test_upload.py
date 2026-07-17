import pytest
import io
import sys
from PIL import Image
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_ocr_status():
    response = client.get("/api/ocr-status")
    assert response.status_code == 200
    data = response.json()
    assert "easyocr" in data
    assert "tesseract" in data

def test_upload_invalid_content_type():
    # Send text file instead of image
    files = {"file": ("test.txt", b"some plain text content", "text/plain")}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 400
    assert "Only JPEG/PNG/WebP images are accepted" in response.json()["detail"]

def test_upload_valid_image(monkeypatch):
    # Create a small valid memory image (PNG)
    img = Image.new("RGB", (100, 100), color="white")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    files = {"file": ("test.png", img_byte_arr.read(), "image/png")}

    # Mock extract_text robustly across any sys.modules naming (routers.upload / backend.routers.upload)
    import backend.routers.upload as upload_router
    monkeypatch.setattr(upload_router, "extract_text", lambda img: ["Doloo 650", "Azithraal 500"])

    if "routers.upload" in sys.modules:
        monkeypatch.setattr(sys.modules["routers.upload"], "extract_text", lambda img: ["Doloo 650", "Azithraal 500"])

    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "ocr_status" in data
    assert data["raw_texts"] == ["Doloo 650", "Azithraal 500"]
    assert len(data["matches"]) > 0

    # Matches should be ordered by confidence score
    first_match = data["matches"][0]
    assert "ocr_text" in first_match
    assert "matched_name" in first_match
    assert "confidence" in first_match
    assert "confidence_label" in first_match
    assert "medicine_info" in first_match

def test_upload_empty_ocr(monkeypatch):
    # Create a small valid memory image (PNG)
    img = Image.new("RGB", (100, 100), color="white")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    files = {"file": ("test.png", img_byte_arr.read(), "image/png")}

    # Mock extract_text to return absolutely nothing
    import backend.routers.upload as upload_router
    monkeypatch.setattr(upload_router, "extract_text", lambda img: [])

    if "routers.upload" in sys.modules:
        monkeypatch.setattr(sys.modules["routers.upload"], "extract_text", lambda img: [])

    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "No text could be extracted" in data["message"]
    assert data["raw_texts"] == []
    assert data["matches"] == []


def test_upload_image_with_metadata():
    # Create an image with prescription text in PNG metadata
    from PIL import PngImagePlugin
    img = Image.new("RGB", (100, 100), color="white")
    meta = PngImagePlugin.PngInfo()
    meta.add_text("prescription_text", "Dolo 650, Azithral 500")

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG", pnginfo=meta)
    img_byte_arr.seek(0)

    files = {"file": ("test_metadata.png", img_byte_arr.read(), "image/png")}

    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # It should have extracted the exact text from the PNG info
    assert "Dolo 650" in data["raw_texts"]
    assert "Azithral 500" in data["raw_texts"]
    assert len(data["matches"]) >= 2
