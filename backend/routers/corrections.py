from fastapi import APIRouter
from pydantic import BaseModel
from database import save_correction, get_corrections

router = APIRouter()


class CorrectionRequest(BaseModel):
    ocr_text: str
    system_guess: str = None
    user_correction: str
    confidence: float = 0.0


@router.post('/corrections')
def submit_correction(req: CorrectionRequest):
    """Submit a user correction for OCR/matching results."""
    save_correction(req.ocr_text, req.system_guess, req.user_correction, req.confidence)
    return {'status': 'success', 'message': 'Correction recorded. Thank you!'}


@router.get('/corrections')
def list_corrections():
    """List all submitted corrections."""
    return get_corrections()
