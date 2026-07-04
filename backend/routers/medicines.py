from fastapi import APIRouter, Query
from database import get_all_medicines, search_medicines

router = APIRouter()


@router.get('/medicines')
def list_medicines(q: str = Query(None, description='Search query')):
    """List all medicines or search by name/generic name."""
    if q:
        return search_medicines(q)
    return get_all_medicines()
