from rapidfuzz import fuzz


def calculate_confidence(ocr_text: str, matched: str, base: float) -> float:
    """Calculate weighted confidence score from multiple similarity metrics."""
    s1 = base / 100.0
    s2 = fuzz.token_sort_ratio(ocr_text, matched) / 100.0
    s3 = fuzz.partial_ratio(ocr_text, matched) / 100.0
    len_diff = abs(len(ocr_text) - len(matched))
    s4 = max(0.0, 1.0 - len_diff / max(len(ocr_text), len(matched), 1))
    return round((s1 * 0.5) + (s2 * 0.2) + (s3 * 0.2) + (s4 * 0.1), 3)


def get_label(conf: float) -> str:
    """Return human-readable confidence label."""
    if conf >= 0.85:
        return 'HIGH'
    elif conf >= 0.60:
        return 'MEDIUM'
    elif conf >= 0.40:
        return 'LOW'
    return 'VERY LOW'
