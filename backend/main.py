import sys
import os
import logging

# Add backend dir to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, medicines, pharmacies, corrections
from database import init_db, seed_medicines

app = FastAPI(
    title='RxVision AI API',
    description='AI-powered prescription reader and medicine identification system',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(upload.router, prefix='/api', tags=['Upload'])
app.include_router(medicines.router, prefix='/api', tags=['Medicines'])
app.include_router(pharmacies.router, prefix='/api', tags=['Pharmacies'])
app.include_router(corrections.router, prefix='/api', tags=['Corrections'])


@app.on_event('startup')
async def startup():
    logger.info('Initializing RxVision AI...')
    init_db()
    seed_medicines()
    logger.info('RxVision AI is ready!')


@app.get('/')
def root():
    return {
        'message': 'RxVision AI is running!',
        'version': '1.0.0',
        'docs': '/docs',
        'endpoints': {
            'upload': '/api/upload',
            'medicines': '/api/medicines',
            'pharmacies': '/api/pharmacies',
            'corrections': '/api/corrections'
        }
    }
