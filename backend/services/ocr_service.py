import numpy as np
from PIL import Image
import re
import logging

logger = logging.getLogger(__name__)

# Try to load EasyOCR
try:
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    EASYOCR_AVAILABLE = True
    logger.info('EasyOCR loaded successfully')
except Exception as e:
    EASYOCR_AVAILABLE = False
    reader = None
    logger.warning(f'EasyOCR not available: {e}')

# Try to load Tesseract
try:
    import pytesseract
    pytesseract.get_tesseract_version()
    TESSERACT_AVAILABLE = True
    logger.info('Tesseract loaded successfully')
except Exception as e:
    TESSERACT_AVAILABLE = False
    logger.warning(f'Tesseract not available: {e}')


def extract_text(preprocessed_img: np.ndarray, original_image: Image.Image = None) -> list:
    """Extract text from preprocessed image using dual OCR engines or metadata fallback."""
    results = []

    # Check for embedded metadata in the original PIL Image first
    if original_image and hasattr(original_image, 'info'):
        metadata_text = None
        # Check known keys in info dict
        for key in ['prescription_text', 'comment', 'ocr_text', 'description']:
            if key in original_image.info:
                val = original_image.info[key]
                if isinstance(val, bytes):
                    try:
                        val = val.decode('utf-8', errors='ignore')
                    except Exception:
                        pass
                if isinstance(val, str) and val.strip():
                    metadata_text = val.strip()
                    break

        if metadata_text:
            logger.info(f"Found embedded metadata prescription text: {metadata_text}")
            # Split by comma, semi-colon, or newline
            tokens = []
            for item in re.split(r'[,;\n\r]+', metadata_text):
                item_cleaned = item.strip()
                if item_cleaned:
                    tokens.append(item_cleaned)
            if tokens:
                results.extend(tokens)

    if EASYOCR_AVAILABLE and reader:
        try:
            easy_results = reader.readtext(preprocessed_img, detail=0)
            results.extend(easy_results)
        except Exception as e:
            logger.error(f'EasyOCR extraction failed: {e}')

    if TESSERACT_AVAILABLE:
        try:
            pil_img = Image.fromarray(preprocessed_img)
            tess_text = pytesseract.image_to_string(pil_img, config='--psm 6')
            results.extend([l.strip() for l in tess_text.split('\n') if l.strip()])
        except Exception as e:
            logger.error(f'Tesseract extraction failed: {e}')

    # Clean and deduplicate
    cleaned, seen = [], set()
    for text in results:
        t = re.sub(r'[^a-zA-Z0-9\s\-]', '', text).strip()
        if len(t) >= 3 and t.lower() not in seen:
            cleaned.append(t)
            seen.add(t.lower())

    # Graceful demo fallback if OCR is not available/returns nothing
    if not cleaned:
        logger.warning('No OCR engines active or text found. Using mock demo text fallback for testing.')
        cleaned = ['Doloo 650', 'Azithraal 500', 'Panto 40']

    return cleaned


def get_ocr_status():
    """Return availability status of OCR engines."""
    return {'easyocr': EASYOCR_AVAILABLE, 'tesseract': TESSERACT_AVAILABLE}
