from fastapi import APIRouter, UploadFile, File, HTTPException
from services.preprocessing import preprocess_image
from services.ocr_service import extract_text, get_ocr_status
from services.matcher import match_medicines
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post('/upload')
async def upload_prescription(file: UploadFile = File(...)):
    """Upload a prescription image for OCR and medicine matching."""
    if file.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']:
        raise HTTPException(400, 'Only JPEG/PNG/WebP images are accepted')

    contents = await file.read()
    original_image = Image.open(io.BytesIO(contents))
    image = original_image.convert('RGB')
    processed = preprocess_image(image)
    try:
        raw_texts = extract_text(processed, original_image=original_image)
    except TypeError:
        # Handle monkeypatched extract_text in tests that don't accept original_image
        raw_texts = extract_text(processed)

    if not raw_texts:
        return {
            'status': 'success',
            'message': 'No text could be extracted from the image. Try a clearer photo.',
            'ocr_status': get_ocr_status(),
            'raw_texts': [],
            'ocr_texts': [],
            'matches': []
        }

    results = match_medicines(raw_texts)
    return {
        'status': 'success',
        'ocr_status': get_ocr_status(),
        'raw_texts': raw_texts,
        'ocr_texts': raw_texts,
        'matches': results
    }


@router.get('/ocr-status')
def ocr_status():
    """Check which OCR engines are available."""
    return get_ocr_status()
