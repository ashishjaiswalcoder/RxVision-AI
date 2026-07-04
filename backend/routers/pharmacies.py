from fastapi import APIRouter, Query
import os
import math
import random

router = APIRouter()

PHARMACY_NAMES = [
    'Apollo Pharmacy', 'MedPlus', 'Netmeds Store', 'Wellness Forever',
    'Frank Ross Pharmacy', 'Guardian Pharmacy', 'Jan Aushadhi Kendra',
    'Sanjivani Medical Store', 'LifeCare Pharmacy', 'Health & Glow',
    'Noble Plus Pharmacy', 'Dawai Dost', 'City Medical Store',
    'Shree Medical Agency', 'Pharma Easy Store', 'Care Chemist',
    'Fortis Pharmacy', 'Max Health Pharmacy', 'Patanjali Megastore',
    'Himalaya Wellness Store'
]


def generate_mock_pharmacies(lat: float, lng: float, radius: int = 1500, count: int = 8):
    """Generate mock pharmacy data around a given location."""
    pharmacies = []
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(100, radius)
        dlat = (dist / 111320) * math.cos(angle)
        dlng = (dist / (111320 * math.cos(math.radians(lat)))) * math.sin(angle)
        pharmacies.append({
            'id': i + 1,
            'name': random.choice(PHARMACY_NAMES),
            'address': f'{random.randint(1, 500)}, Main Road, Near {random.choice(["Bus Stand", "Railway Station", "Hospital", "Market", "Temple", "School"])}',
            'lat': round(lat + dlat, 6),
            'lng': round(lng + dlng, 6),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'open_now': random.choice([True, True, True, False]),
            'distance_m': round(dist)
        })
    pharmacies.sort(key=lambda x: x['distance_m'])
    return pharmacies


@router.get('/pharmacies')
def get_pharmacies(
    lat: float = Query(..., description='Latitude'),
    lng: float = Query(..., description='Longitude'),
    radius: int = Query(1500, description='Search radius in meters')
):
    """Get nearby pharmacies using Google Maps API or mock data."""
    GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    if GOOGLE_MAPS_KEY:
        import requests
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'location': f'{lat},{lng}',
            'radius': radius,
            'type': 'pharmacy',
            'key': GOOGLE_MAPS_KEY
        }
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for p in data.get('results', []):
                loc = p.get('geometry', {}).get('location', {})
                results.append({
                    'id': p.get('place_id'),
                    'name': p.get('name'),
                    'address': p.get('vicinity', ''),
                    'lat': loc.get('lat'),
                    'lng': loc.get('lng'),
                    'rating': p.get('rating', 0),
                    'open_now': p.get('opening_hours', {}).get('open_now', None),
                })
            return results
    return generate_mock_pharmacies(lat, lng, radius)
