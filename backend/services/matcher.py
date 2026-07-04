from rapidfuzz import process, fuzz
from database import get_all_medicines
from services.confidence import calculate_confidence


def match_medicines(ocr_texts: list) -> list:
    """Match OCR-extracted texts against medicine database using fuzzy matching."""
    medicines = get_all_medicines()
    name_map = {}

    for m in medicines:
        name_map[m['medicine_name'].lower()] = m
        if m.get('aliases'):
            for alias in m['aliases'].split(','):
                a = alias.strip()
                if a:
                    name_map[a.lower()] = m

    all_names = list(name_map.keys())
    all_matches = []
    seen_medicines = set()

    for text in ocr_texts:
        if len(text) < 3:
            continue
        matches = process.extract(text.lower(), all_names, scorer=fuzz.WRatio, limit=3)
        for match_name, score, idx in matches:
            if score >= 40:
                med = name_map[match_name]
                med_id = med.get('id', med['medicine_name'])
                if med_id in seen_medicines:
                    continue
                seen_medicines.add(med_id)
                conf = calculate_confidence(text, match_name, score)
                all_matches.append({
                    'ocr_text': text,
                    'matched_name': med['medicine_name'],
                    'confidence': conf,
                    'confidence_label': (
                        'HIGH' if conf >= 0.85
                        else 'MEDIUM' if conf >= 0.60
                        else 'LOW' if conf >= 0.40
                        else 'VERY LOW'
                    ),
                    'medicine_info': {
                        'id': med.get('id'),
                        'medicine_name': med['medicine_name'],
                        'generic_name': med['generic_name'],
                        'company_name': med.get('company_name', 'Unknown'),
                        'dosage_form': med['dosage_form'],
                        'aliases': med.get('aliases', '')
                    }
                })

    all_matches.sort(key=lambda x: x['confidence'], reverse=True)
    return all_matches[:10]
