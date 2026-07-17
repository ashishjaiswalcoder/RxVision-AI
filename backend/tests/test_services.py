import pytest
import numpy as np
from PIL import Image
from backend.services.preprocessing import preprocess_image
from backend.services.confidence import calculate_confidence, get_label
from backend.services.matcher import match_medicines

def test_preprocess_image():
    # Create dummy white/black image
    img = Image.new("RGB", (50, 50), color="white")
    processed = preprocess_image(img)
    assert isinstance(processed, np.ndarray)
    # The preprocessing steps include resizing (fx=2, fy=2)
    assert processed.shape == (100, 100)

def test_calculate_confidence_perfect():
    # Exact match should result in high score
    score = calculate_confidence("Dolo 650", "Dolo 650", 100.0)
    assert score == 1.0
    assert get_label(score) == "HIGH"

def test_calculate_confidence_close():
    # Sightly different match
    score = calculate_confidence("Doloo 650", "Dolo 650", 90.0)
    assert 0.5 < score < 1.0
    label = get_label(score)
    assert label in ["HIGH", "MEDIUM", "LOW"]

def test_calculate_confidence_poor():
    # Totally different match
    score = calculate_confidence("Xyz", "Dolo 650", 10.0)
    assert score < 0.40
    assert get_label(score) == "VERY LOW"

def test_match_medicines_exact():
    # Standard medicine from the database
    matches = match_medicines(["Dolo 650"])
    assert len(matches) > 0
    # First match should be Dolo 650
    assert matches[0]["matched_name"] == "Dolo 650"
    assert matches[0]["confidence_label"] == "HIGH"

def test_match_medicines_fuzzy():
    # Slightly misspelled
    matches = match_medicines(["Doloo 650"])
    assert len(matches) > 0
    # Should still match Dolo 650
    assert matches[0]["matched_name"] == "Dolo 650"

def test_match_medicines_no_match():
    # Non-existent and short string
    matches = match_medicines(["X"])
    assert len(matches) == 0
