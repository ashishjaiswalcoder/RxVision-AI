import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'medicines.db')


@contextmanager
def get_db():
    """Context manager for database connections."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create database tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_name TEXT NOT NULL,
                generic_name TEXT NOT NULL,
                company_name TEXT DEFAULT 'Unknown',
                dosage_form TEXT DEFAULT 'Tablet',
                aliases TEXT DEFAULT ''
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS corrections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ocr_text TEXT NOT NULL,
                system_guess TEXT,
                user_correction TEXT NOT NULL,
                confidence REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')


def seed_medicines():
    """Seed the medicines table with 200+ common Indian medicines if empty."""
    with get_db() as conn:
        count = conn.execute('SELECT COUNT(*) FROM medicines').fetchone()[0]
        if count > 0:
            return

        medicines = [
            # === ANALGESICS / ANTIPYRETICS ===
            ('Crocin 500mg', 'Paracetamol', 'GSK', 'Tablet', 'PCM,Para,Crocin'),
            ('Dolo 650', 'Paracetamol', 'Micro Labs', 'Tablet', 'Dolo,Paracetamol 650'),
            ('Calpol 500', 'Paracetamol', 'GSK', 'Tablet', 'Calpol'),
            ('Combiflam', 'Ibuprofen+Paracetamol', 'Sanofi', 'Tablet', 'Combiflam'),
            ('Saridon', 'Propyphenazone+Paracetamol+Caffeine', 'Bayer', 'Tablet', 'Saridon'),
            ('Sumo', 'Nimesulide+Paracetamol', 'Alkem', 'Tablet', 'Sumo'),
            ('Voveran 50', 'Diclofenac', 'Novartis', 'Tablet', 'Voveran,Diclofenac'),
            ('Voveran SR 100', 'Diclofenac SR', 'Novartis', 'Tablet', 'Voveran SR'),
            ('Brufen 400', 'Ibuprofen', 'Abbott', 'Tablet', 'Brufen,Ibuprofen'),
            ('Nise', 'Nimesulide', 'Dr Reddys', 'Tablet', 'Nise,Nimesulide'),
            ('Flexon', 'Ibuprofen+Paracetamol', 'Aristo', 'Tablet', 'Flexon'),
            ('Zerodol SP', 'Aceclofenac+Paracetamol+Serratiopeptidase', 'IPCA', 'Tablet', 'Zerodol,Zerodol SP'),
            ('Zerodol P', 'Aceclofenac+Paracetamol', 'IPCA', 'Tablet', 'Zerodol P'),
            ('Hifenac P', 'Aceclofenac+Paracetamol', 'Intas', 'Tablet', 'Hifenac,Hifenac P'),
            ('Ultracet', 'Tramadol+Paracetamol', 'Johnson & Johnson', 'Tablet', 'Ultracet'),
            ('Meftal Spas', 'Mefenamic Acid+Dicyclomine', 'Blue Cross', 'Tablet', 'Meftal,Meftal Spas'),
            ('Meftal Forte', 'Mefenamic Acid+Paracetamol', 'Blue Cross', 'Tablet', 'Meftal Forte'),

            # === ANTIBIOTICS ===
            ('Azithral 500', 'Azithromycin', 'Alembic', 'Tablet', 'Azithral,Azee'),
            ('Azee 500', 'Azithromycin', 'Cipla', 'Tablet', 'Azee 500'),
            ('Augmentin 625 Duo', 'Amoxicillin+Clavulanate', 'GSK', 'Tablet', 'Augmentin,Augmentin 625'),
            ('Mox 500', 'Amoxicillin', 'Ranbaxy', 'Capsule', 'Mox,Amoxicillin'),
            ('Mox CV 625', 'Amoxicillin+Clavulanate', 'Ranbaxy', 'Tablet', 'Mox CV'),
            ('Ciprofloxacin 500', 'Ciprofloxacin', 'Cipla', 'Tablet', 'Cipro,Ciplox'),
            ('Ciplox 500', 'Ciprofloxacin', 'Cipla', 'Tablet', 'Ciplox 500'),
            ('Ciplox TZ', 'Ciprofloxacin+Tinidazole', 'Cipla', 'Tablet', 'Ciplox TZ'),
            ('Oflox 200', 'Ofloxacin', 'Cipla', 'Tablet', 'Oflox,Ofloxacin'),
            ('Oflox OZ', 'Ofloxacin+Ornidazole', 'Cipla', 'Tablet', 'Oflox OZ'),
            ('Taxim O 200', 'Cefixime', 'Alkem', 'Tablet', 'Taxim,Cefixime'),
            ('Zifi 200', 'Cefixime', 'FDC', 'Tablet', 'Zifi,Zifi 200'),
            ('Monocef 200', 'Cefpodoxime', 'Aristo', 'Tablet', 'Monocef'),
            ('Cefspan 200', 'Cefixime', 'Lupin', 'Capsule', 'Cefspan'),
            ('Clavam 625', 'Amoxicillin+Clavulanate', 'Alkem', 'Tablet', 'Clavam'),
            ('Levoflox 500', 'Levofloxacin', 'Cipla', 'Tablet', 'Levoflox,Levofloxacin'),
            ('Levofloxacin 750', 'Levofloxacin', 'Cipla', 'Tablet', 'Levoflox 750'),
            ('Norflox TZ', 'Norfloxacin+Tinidazole', 'Cipla', 'Tablet', 'Norflox TZ'),
            ('Metrogyl 400', 'Metronidazole', 'J&J', 'Tablet', 'Metrogyl,Flagyl'),
            ('Flagyl 400', 'Metronidazole', 'Sanofi', 'Tablet', 'Flagyl 400'),
            ('Bactrim DS', 'Sulfamethoxazole+Trimethoprim', 'Roche', 'Tablet', 'Bactrim,Septran'),
            ('Septran DS', 'Sulfamethoxazole+Trimethoprim', 'GSK', 'Tablet', 'Septran DS'),
            ('Doxycycline 100', 'Doxycycline', 'Cipla', 'Capsule', 'Doxy,Doxycycline'),
            ('Cephalexin 500', 'Cephalexin', 'Lupin', 'Capsule', 'Cephalexin,Sporidex'),
            ('Sporidex 500', 'Cephalexin', 'Sun Pharma', 'Capsule', 'Sporidex 500'),
            ('Clindamycin 300', 'Clindamycin', 'Cipla', 'Capsule', 'Clindamycin'),
            ('Linezolid 600', 'Linezolid', 'Glenmark', 'Tablet', 'Linezolid,Lizolid'),
            ('Clarithromycin 500', 'Clarithromycin', 'Abbott', 'Tablet', 'Clarithromycin'),

            # === GASTROINTESTINAL ===
            ('Pan 40', 'Pantoprazole', 'Alkem', 'Tablet', 'Pan,Pantop'),
            ('Pantop 40', 'Pantoprazole', 'Aristo', 'Tablet', 'Pantop 40'),
            ('Pan D', 'Pantoprazole+Domperidone', 'Alkem', 'Capsule', 'Pan D'),
            ('Pantocid', 'Pantoprazole', 'Sun Pharma', 'Tablet', 'Pantocid'),
            ('Pantocid DSR', 'Pantoprazole+Domperidone SR', 'Sun Pharma', 'Capsule', 'Pantocid DSR'),
            ('Omez 20', 'Omeprazole', 'Dr Reddys', 'Capsule', 'Omez,Omeprazole'),
            ('Omez D', 'Omeprazole+Domperidone', 'Dr Reddys', 'Capsule', 'Omez D'),
            ('Razo 20', 'Rabeprazole', 'Dr Reddys', 'Tablet', 'Razo,Rabeprazole'),
            ('Razo D', 'Rabeprazole+Domperidone', 'Dr Reddys', 'Capsule', 'Razo D'),
            ('Rantac 150', 'Ranitidine', 'J&J', 'Tablet', 'Rantac,Ranitidine'),
            ('Aciloc 150', 'Ranitidine', 'Cadila', 'Tablet', 'Aciloc'),
            ('Gelusil MPS', 'Aluminium Hydroxide+Magnesium Hydroxide', 'Pfizer', 'Suspension', 'Gelusil'),
            ('Digene', 'Aluminium Hydroxide+Magnesium Hydroxide+Simethicone', 'Abbott', 'Tablet', 'Digene'),
            ('Duphalac', 'Lactulose', 'Abbott', 'Syrup', 'Duphalac,Lactulose'),
            ('Cremaffin', 'Liquid Paraffin+Magnesium Hydroxide', 'Abbott', 'Syrup', 'Cremaffin'),
            ('Gutwell', 'Probiotics', 'Alkem', 'Capsule', 'Gutwell'),
            ('Econorm', 'Saccharomyces Boulardii', 'Dr Reddys', 'Capsule', 'Econorm'),
            ('Norflox TZ', 'Norfloxacin+Tinidazole', 'Cipla', 'Tablet', 'Norflox'),
            ('Domstal 10', 'Domperidone', 'Torrent', 'Tablet', 'Domstal,Domperidone'),
            ('Emeset 4', 'Ondansetron', 'Cipla', 'Tablet', 'Emeset,Ondansetron'),
            ('Perinorm', 'Metoclopramide', 'IPCA', 'Tablet', 'Perinorm'),
            ('Sucralfate O2', 'Sucralfate+Oxetacaine', 'Abbott', 'Suspension', 'Sucralfate'),
            ('Mucaine Gel', 'Oxetacaine+Aluminium Hydroxide+Magnesium Hydroxide', 'Pfizer', 'Gel', 'Mucaine'),

            # === ANTIHYPERTENSIVES ===
            ('Telma 40', 'Telmisartan', 'Glenmark', 'Tablet', 'Telma,Telmisartan'),
            ('Telma H', 'Telmisartan+Hydrochlorothiazide', 'Glenmark', 'Tablet', 'Telma H'),
            ('Telma AM', 'Telmisartan+Amlodipine', 'Glenmark', 'Tablet', 'Telma AM'),
            ('Amlong 5', 'Amlodipine', 'Micro Labs', 'Tablet', 'Amlong,Amlodipine'),
            ('Amlong 10', 'Amlodipine', 'Micro Labs', 'Tablet', 'Amlong 10'),
            ('Amlokind AT', 'Amlodipine+Atenolol', 'Mankind', 'Tablet', 'Amlokind'),
            ('Stamlo 5', 'Amlodipine', 'Dr Reddys', 'Tablet', 'Stamlo'),
            ('Aten 50', 'Atenolol', 'Zydus', 'Tablet', 'Aten,Atenolol'),
            ('Metolar 50', 'Metoprolol', 'Cipla', 'Tablet', 'Metolar,Metoprolol'),
            ('Metolar XR 50', 'Metoprolol XR', 'Cipla', 'Tablet', 'Metolar XR'),
            ('Nebicard 5', 'Nebivolol', 'Torrent', 'Tablet', 'Nebicard,Nebivolol'),
            ('Losar 50', 'Losartan', 'Cipla', 'Tablet', 'Losar,Losartan'),
            ('Losar H', 'Losartan+Hydrochlorothiazide', 'Cipla', 'Tablet', 'Losar H'),
            ('Covance 50', 'Losartan', 'Ranbaxy', 'Tablet', 'Covance'),
            ('Ramipril 5', 'Ramipril', 'Sanofi', 'Tablet', 'Ramipril,Cardace'),
            ('Cardace 5', 'Ramipril', 'Sanofi', 'Tablet', 'Cardace 5'),
            ('Enalapril 5', 'Enalapril', 'Cadila', 'Tablet', 'Enalapril,Envas'),
            ('Envas 5', 'Enalapril', 'Cadila', 'Tablet', 'Envas 5'),
            ('Prazopress 2.5', 'Prazosin', 'Cipla', 'Tablet', 'Prazopress'),
            ('Minipress XL 5', 'Prazosin XL', 'Pfizer', 'Tablet', 'Minipress'),
            ('Concor 5', 'Bisoprolol', 'Merck', 'Tablet', 'Concor,Bisoprolol'),
            ('Cilacar 10', 'Cilnidipine', 'J&J', 'Tablet', 'Cilacar,Cilnidipine'),

            # === CARDIOVASCULAR ===
            ('Ecosprin 75', 'Aspirin', 'USV', 'Tablet', 'Ecosprin,Aspirin'),
            ('Ecosprin AV 75/20', 'Aspirin+Atorvastatin', 'USV', 'Capsule', 'Ecosprin AV'),
            ('Ecosprin Gold', 'Aspirin+Atorvastatin+Clopidogrel', 'USV', 'Capsule', 'Ecosprin Gold'),
            ('Clopidogrel 75', 'Clopidogrel', 'USV', 'Tablet', 'Clopidogrel,Clopilet'),
            ('Clopilet 75', 'Clopidogrel', 'Sun Pharma', 'Tablet', 'Clopilet 75'),
            ('Atorva 10', 'Atorvastatin', 'Zydus', 'Tablet', 'Atorva,Atorvastatin'),
            ('Atorva 20', 'Atorvastatin', 'Zydus', 'Tablet', 'Atorva 20'),
            ('Atorva 40', 'Atorvastatin', 'Zydus', 'Tablet', 'Atorva 40'),
            ('Rosuvas 10', 'Rosuvastatin', 'Sun Pharma', 'Tablet', 'Rosuvas,Rosuvastatin'),
            ('Rosuvas 20', 'Rosuvastatin', 'Sun Pharma', 'Tablet', 'Rosuvas 20'),
            ('Rozavel 10', 'Rosuvastatin', 'Sun Pharma', 'Tablet', 'Rozavel'),
            ('Sorbitrate 5', 'Isosorbide Dinitrate', 'Sun Pharma', 'Tablet', 'Sorbitrate'),
            ('Dilzem 30', 'Diltiazem', 'Torrent', 'Tablet', 'Dilzem,Diltiazem'),
            ('Arkamin 0.1', 'Clonidine', 'Torrent', 'Tablet', 'Arkamin,Clonidine'),
            ('Dytor 10', 'Torsemide', 'Cipla', 'Tablet', 'Dytor,Torsemide'),
            ('Lasix 40', 'Furosemide', 'Sanofi', 'Tablet', 'Lasix,Furosemide'),
            ('Aldactone 25', 'Spironolactone', 'RPG', 'Tablet', 'Aldactone,Spironolactone'),

            # === ANTIDIABETICS ===
            ('Glycomet GP 2', 'Metformin+Glimepiride', 'USV', 'Tablet', 'Glycomet GP,Glycomet'),
            ('Glycomet 500', 'Metformin', 'USV', 'Tablet', 'Glycomet 500'),
            ('Glycomet SR 500', 'Metformin SR', 'USV', 'Tablet', 'Glycomet SR'),
            ('Gluconorm G2', 'Metformin+Glimepiride', 'Lupin', 'Tablet', 'Gluconorm'),
            ('Amaryl M2', 'Metformin+Glimepiride', 'Sanofi', 'Tablet', 'Amaryl,Amaryl M'),
            ('Janumet 50/500', 'Sitagliptin+Metformin', 'MSD', 'Tablet', 'Janumet'),
            ('Januvia 100', 'Sitagliptin', 'MSD', 'Tablet', 'Januvia'),
            ('Galvus Met 50/500', 'Vildagliptin+Metformin', 'Novartis', 'Tablet', 'Galvus Met'),
            ('Jalra M 50/500', 'Vildagliptin+Metformin', 'USV', 'Tablet', 'Jalra M'),
            ('Trajenta 5', 'Linagliptin', 'Boehringer Ingelheim', 'Tablet', 'Trajenta,Linagliptin'),
            ('Jardiance 10', 'Empagliflozin', 'Boehringer Ingelheim', 'Tablet', 'Jardiance,Empagliflozin'),
            ('Forxiga 10', 'Dapagliflozin', 'AstraZeneca', 'Tablet', 'Forxiga,Dapagliflozin'),
            ('Invokana 100', 'Canagliflozin', 'Johnson & Johnson', 'Tablet', 'Invokana'),
            ('Glynase MF', 'Metformin+Glipizide', 'USV', 'Tablet', 'Glynase'),
            ('Glimy 2', 'Glimepiride', 'USV', 'Tablet', 'Glimy,Glimepiride'),
            ('Daonil 5', 'Glibenclamide', 'Sanofi', 'Tablet', 'Daonil'),
            ('Pioz 15', 'Pioglitazone', 'USV', 'Tablet', 'Pioz,Pioglitazone'),
            ('Voglibose 0.3', 'Voglibose', 'Ranbaxy', 'Tablet', 'Voglibose,Vogli'),
            ('Lantus', 'Insulin Glargine', 'Sanofi', 'Injection', 'Lantus'),
            ('Mixtard 30', 'Human Insulin 30/70', 'Novo Nordisk', 'Injection', 'Mixtard'),

            # === RESPIRATORY ===
            ('Asthalin Inhaler', 'Salbutamol', 'Cipla', 'Inhaler', 'Asthalin,Salbutamol'),
            ('Budecort 200', 'Budesonide', 'Cipla', 'Inhaler', 'Budecort,Budesonide'),
            ('Seroflo 250', 'Salmeterol+Fluticasone', 'Cipla', 'Inhaler', 'Seroflo'),
            ('Foracort 200', 'Formoterol+Budesonide', 'Cipla', 'Inhaler', 'Foracort'),
            ('Deriphyllin', 'Etofylline+Theophylline', 'Abbott', 'Tablet', 'Deriphyllin'),
            ('Montair LC', 'Montelukast+Levocetirizine', 'Cipla', 'Tablet', 'Montair LC'),
            ('Montair 10', 'Montelukast', 'Cipla', 'Tablet', 'Montair,Montelukast'),
            ('Sinarest', 'Paracetamol+Phenylephrine+Chlorpheniramine', 'Centaur', 'Tablet', 'Sinarest'),
            ('Alex', 'Phenylephrine+Chlorpheniramine+Dextromethorphan', 'Glenmark', 'Syrup', 'Alex'),
            ('Benadryl', 'Diphenhydramine', 'Johnson & Johnson', 'Syrup', 'Benadryl'),
            ('Grilinctus', 'Dextromethorphan+Phenylephrine+CPM', 'Franco Indian', 'Syrup', 'Grilinctus'),
            ('Ascoril LS', 'Ambroxol+Levosalbutamol+Guaifenesin', 'Glenmark', 'Syrup', 'Ascoril'),
            ('Cheston Cold', 'Paracetamol+Phenylephrine+Cetirizine+Caffeine', 'Cipla', 'Tablet', 'Cheston'),
            ('Mucinac 600', 'Acetylcysteine', 'Cipla', 'Tablet', 'Mucinac'),
            ('Ambrodil S', 'Ambroxol+Salbutamol', 'Aristo', 'Syrup', 'Ambrodil'),
            ('Tiova 18', 'Tiotropium', 'Cipla', 'Inhaler', 'Tiova,Tiotropium'),

            # === ANTIHISTAMINES / ANTI-ALLERGICS ===
            ('Allegra 120', 'Fexofenadine', 'Sanofi', 'Tablet', 'Allegra,Fexofenadine'),
            ('Allegra 180', 'Fexofenadine', 'Sanofi', 'Tablet', 'Allegra 180'),
            ('Cetirizine 10', 'Cetirizine', 'Cipla', 'Tablet', 'Cetirizine,Cetzine'),
            ('Cetzine', 'Cetirizine', 'Dr Reddys', 'Tablet', 'Cetzine 10'),
            ('Levocet', 'Levocetirizine', 'Sun Pharma', 'Tablet', 'Levocet,Levocetirizine'),
            ('Okacet', 'Cetirizine', 'Cipla', 'Tablet', 'Okacet'),
            ('Avil 25', 'Pheniramine', 'Sanofi', 'Tablet', 'Avil,Pheniramine'),
            ('Montek LC', 'Montelukast+Levocetirizine', 'Sun Pharma', 'Tablet', 'Montek LC'),
            ('Bilastine 20', 'Bilastine', 'Sun Pharma', 'Tablet', 'Bilastine'),
            ('Hydroxyzine 25', 'Hydroxyzine', 'UCB', 'Tablet', 'Hydroxyzine,Atarax'),
            ('Atarax 25', 'Hydroxyzine', 'UCB', 'Tablet', 'Atarax 25'),

            # === VITAMINS / MINERALS / SUPPLEMENTS ===
            ('Shelcal 500', 'Calcium+Vitamin D3', 'Torrent', 'Tablet', 'Shelcal,Calcium'),
            ('Shelcal HD', 'Calcium+Vitamin D3', 'Torrent', 'Tablet', 'Shelcal HD'),
            ('Supradyn', 'Multivitamins+Minerals', 'Bayer', 'Tablet', 'Supradyn'),
            ('Becosules', 'B Complex+Vitamin C', 'Pfizer', 'Capsule', 'Becosules,B Complex'),
            ('Becosules Z', 'B Complex+Vitamin C+Zinc', 'Pfizer', 'Capsule', 'Becosules Z'),
            ('Limcee 500', 'Vitamin C', 'Abbott', 'Tablet', 'Limcee,Vitamin C'),
            ('Zincovit', 'Multivitamins+Zinc', 'Apex', 'Tablet', 'Zincovit'),
            ('Revital H', 'Multivitamins+Minerals+Ginseng', 'Sun Pharma', 'Capsule', 'Revital'),
            ('Neurobion Forte', 'Vitamin B1+B6+B12', 'Merck', 'Tablet', 'Neurobion'),
            ('Methylcobal 1500', 'Methylcobalamin', 'Aristo', 'Tablet', 'Methylcobal'),
            ('Nurokind Plus', 'Methylcobalamin+Alpha Lipoic Acid+Folic Acid', 'Mankind', 'Tablet', 'Nurokind'),
            ('Folvite 5', 'Folic Acid', 'Pfizer', 'Tablet', 'Folvite,Folic Acid'),
            ('Calcirol D3', 'Cholecalciferol', 'Cadila', 'Capsule', 'Calcirol,Vitamin D3'),
            ('Uprise D3 60K', 'Cholecalciferol 60000 IU', 'Alkem', 'Capsule', 'Uprise D3'),
            ('Ferium XT', 'Iron+Folic Acid', 'Emcure', 'Tablet', 'Ferium,Iron'),
            ('Orofer XT', 'Iron+Folic Acid', 'Emcure', 'Tablet', 'Orofer'),
            ('Livogen', 'Iron+Folic Acid', 'Merck', 'Tablet', 'Livogen'),
            ('A to Z NS', 'Multivitamins+Minerals', 'Alkem', 'Tablet', 'A to Z'),
            ('Evion 400', 'Vitamin E', 'Merck', 'Capsule', 'Evion,Vitamin E'),
            ('Calcium Sandoz', 'Calcium', 'Novartis', 'Tablet', 'Calcium Sandoz'),
            ('Ostocalcium', 'Calcium+Vitamin D3', 'GSK', 'Tablet', 'Ostocalcium'),
            ('Dydroboon', 'Dydrogesterone', 'Emcure', 'Tablet', 'Dydroboon'),

            # === ANTIFUNGALS ===
            ('Fluconazole 150', 'Fluconazole', 'Cipla', 'Tablet', 'Fluconazole,Zocon'),
            ('Zocon 150', 'Fluconazole', 'FDC', 'Tablet', 'Zocon 150'),
            ('Itraconazole 100', 'Itraconazole', 'Glenmark', 'Capsule', 'Itraconazole,Canditral'),
            ('Canditral 100', 'Itraconazole', 'Glenmark', 'Capsule', 'Canditral 100'),
            ('Terbinafine 250', 'Terbinafine', 'Dr Reddys', 'Tablet', 'Terbinafine'),
            ('Griseofulvin 500', 'Griseofulvin', 'GSK', 'Tablet', 'Griseofulvin,Grisovin'),
            ('Ketoconazole 200', 'Ketoconazole', 'Cipla', 'Tablet', 'Ketoconazole'),

            # === ANTIVIRALS ===
            ('Acyclovir 400', 'Acyclovir', 'Cipla', 'Tablet', 'Acyclovir,Zovirax'),
            ('Valacyclovir 500', 'Valacyclovir', 'Cipla', 'Tablet', 'Valacyclovir,Valcivir'),
            ('Oseltamivir 75', 'Oseltamivir', 'Hetero', 'Capsule', 'Oseltamivir,Tamiflu'),
            ('Favipiravir 200', 'Favipiravir', 'Glenmark', 'Tablet', 'Favipiravir,Fabiflu'),
            ('Molnupiravir 200', 'Molnupiravir', 'Sun Pharma', 'Capsule', 'Molnupiravir'),

            # === DERMATOLOGICAL ===
            ('Betnovate C', 'Betamethasone+Clioquinol', 'GSK', 'Cream', 'Betnovate,Betnovate C'),
            ('Betnovate N', 'Betamethasone+Neomycin', 'GSK', 'Cream', 'Betnovate N'),
            ('Candid B', 'Clotrimazole+Beclometasone', 'Glenmark', 'Cream', 'Candid B'),
            ('Candid Cream', 'Clotrimazole', 'Glenmark', 'Cream', 'Candid'),
            ('Clobetasol Cream', 'Clobetasol', 'Cipla', 'Cream', 'Clobetasol,Tenovate'),
            ('Tenovate', 'Clobetasol', 'GSK', 'Cream', 'Tenovate Cream'),
            ('Quadriderm RF', 'Beclometasone+Clotrimazole+Neomycin', 'Piramal', 'Cream', 'Quadriderm'),
            ('Soframycin', 'Framycetin', 'Sanofi', 'Cream', 'Soframycin'),
            ('Fucidin', 'Fusidic Acid', 'Leo Pharma', 'Cream', 'Fucidin'),
            ('T-Bact', 'Mupirocin', 'GSK', 'Ointment', 'T-Bact,Mupirocin'),
            ('Panderm Plus', 'Clobetasol+Ofloxacin+Ornidazole+Terbinafine', 'Macleods', 'Cream', 'Panderm'),
            ('Momate Cream', 'Mometasone', 'Glenmark', 'Cream', 'Momate'),
            ('Elocon Cream', 'Mometasone', 'MSD', 'Cream', 'Elocon'),

            # === NEUROLOGICAL / PSYCHIATRIC ===
            ('Etizola 0.5', 'Etizolam', 'Sun Pharma', 'Tablet', 'Etizola,Etizolam'),
            ('Clonazepam 0.5', 'Clonazepam', 'Sun Pharma', 'Tablet', 'Clonazepam,Clonotril'),
            ('Clonotril 0.5', 'Clonazepam', 'Torrent', 'Tablet', 'Clonotril 0.5'),
            ('Lonazep 0.5', 'Clonazepam', 'Sun Pharma', 'Tablet', 'Lonazep'),
            ('Gabapin NT', 'Gabapentin+Nortriptyline', 'Intas', 'Tablet', 'Gabapin'),
            ('Pregabalin 75', 'Pregabalin', 'Sun Pharma', 'Capsule', 'Pregabalin,Pregalin'),
            ('Pregalin M 75', 'Pregabalin+Methylcobalamin', 'Torrent', 'Capsule', 'Pregalin M'),
            ('Nexito 10', 'Escitalopram', 'Sun Pharma', 'Tablet', 'Nexito,Escitalopram'),
            ('Nexito Plus', 'Escitalopram+Clonazepam', 'Sun Pharma', 'Tablet', 'Nexito Plus'),
            ('Fluoxetine 20', 'Fluoxetine', 'Sun Pharma', 'Capsule', 'Fluoxetine,Fludac'),
            ('Fludac 20', 'Fluoxetine', 'Intas', 'Capsule', 'Fludac 20'),
            ('Amitriptyline 25', 'Amitriptyline', 'Intas', 'Tablet', 'Amitriptyline,Tryptomer'),
            ('Tryptomer 25', 'Amitriptyline', 'Merind', 'Tablet', 'Tryptomer 25'),
            ('Olanzapine 5', 'Olanzapine', 'Sun Pharma', 'Tablet', 'Olanzapine,Oleanz'),
            ('Oleanz 5', 'Olanzapine', 'Sun Pharma', 'Tablet', 'Oleanz 5'),
            ('Quetiapine 25', 'Quetiapine', 'Sun Pharma', 'Tablet', 'Quetiapine'),
            ('Risperidone 2', 'Risperidone', 'Sun Pharma', 'Tablet', 'Risperidone,Risperdal'),
            ('Phenytoin 100', 'Phenytoin', 'Abbott', 'Tablet', 'Phenytoin,Eptoin'),
            ('Eptoin 100', 'Phenytoin', 'Abbott', 'Tablet', 'Eptoin 100'),
            ('Carbamazepine 200', 'Carbamazepine', 'Sun Pharma', 'Tablet', 'Carbamazepine,Tegrital'),
            ('Tegrital 200', 'Carbamazepine', 'Novartis', 'Tablet', 'Tegrital 200'),
            ('Valproate 200', 'Sodium Valproate', 'Sun Pharma', 'Tablet', 'Valproate,Valparin'),
            ('Valparin 200', 'Sodium Valproate', 'Sanofi', 'Tablet', 'Valparin 200'),
            ('Levetiracetam 500', 'Levetiracetam', 'Sun Pharma', 'Tablet', 'Levetiracetam,Levipil'),
            ('Levipil 500', 'Levetiracetam', 'Sun Pharma', 'Tablet', 'Levipil 500'),
            ('Sertraline 50', 'Sertraline', 'Sun Pharma', 'Tablet', 'Sertraline,Serta'),
            ('Duloxetine 20', 'Duloxetine', 'Sun Pharma', 'Capsule', 'Duloxetine,Duzela'),

            # === CORTICOSTEROIDS ===
            ('Wysolone 5', 'Prednisolone', 'Pfizer', 'Tablet', 'Wysolone,Prednisolone'),
            ('Wysolone 10', 'Prednisolone', 'Pfizer', 'Tablet', 'Wysolone 10'),
            ('Omnacortil 5', 'Prednisolone', 'Macleods', 'Tablet', 'Omnacortil'),
            ('Defcort 6', 'Deflazacort', 'Cipla', 'Tablet', 'Defcort,Deflazacort'),
            ('Dexona', 'Dexamethasone', 'Zydus', 'Tablet', 'Dexona,Dexamethasone'),
            ('Medrol 4', 'Methylprednisolone', 'Pfizer', 'Tablet', 'Medrol'),

            # === OPHTHALMICS ===
            ('Moxifloxacin Eye Drop', 'Moxifloxacin', 'Cipla', 'Eye Drop', 'Moxifloxacin Eye'),
            ('Tobramycin Eye Drop', 'Tobramycin', 'Sun Pharma', 'Eye Drop', 'Tobramycin Eye'),
            ('Lotepred Eye Drop', 'Loteprednol', 'Sun Pharma', 'Eye Drop', 'Lotepred'),
            ('Refresh Tears', 'Carboxymethylcellulose', 'Allergan', 'Eye Drop', 'Refresh Tears'),
            ('Itone Eye Drop', 'Herbal', 'Deys Medical', 'Eye Drop', 'Itone'),
            ('Genteal Eye Drop', 'Hydroxypropyl Methylcellulose', 'Novartis', 'Eye Drop', 'Genteal'),

            # === THYROID ===
            ('Thyronorm 25', 'Levothyroxine', 'Abbott', 'Tablet', 'Thyronorm,Thyroxine'),
            ('Thyronorm 50', 'Levothyroxine', 'Abbott', 'Tablet', 'Thyronorm 50'),
            ('Thyronorm 75', 'Levothyroxine', 'Abbott', 'Tablet', 'Thyronorm 75'),
            ('Thyronorm 100', 'Levothyroxine', 'Abbott', 'Tablet', 'Thyronorm 100'),
            ('Eltroxin 100', 'Levothyroxine', 'GSK', 'Tablet', 'Eltroxin'),
            ('Neomercazole 5', 'Carbimazole', 'Abbott', 'Tablet', 'Neomercazole,Carbimazole'),

            # === MUSCLE RELAXANTS ===
            ('Myospaz Forte', 'Chlorzoxazone+Paracetamol', 'FDC', 'Tablet', 'Myospaz'),
            ('Thiocolchicoside 4', 'Thiocolchicoside', 'Sanofi', 'Capsule', 'Thiocolchicoside,Myoril'),
            ('Myoril 4', 'Thiocolchicoside', 'Sanofi', 'Capsule', 'Myoril 4'),
            ('Tizanidine 2', 'Tizanidine', 'Sun Pharma', 'Tablet', 'Tizanidine,Sirdalud'),
            ('Sirdalud 2', 'Tizanidine', 'Novartis', 'Tablet', 'Sirdalud 2'),
            ('Cyclopam', 'Dicyclomine+Paracetamol', 'Indoco', 'Tablet', 'Cyclopam'),
            ('Drotaverine 80', 'Drotaverine', 'Abbott', 'Tablet', 'Drotaverine,Drotin'),
            ('Drotin DS', 'Drotaverine', 'Walter Bushnell', 'Tablet', 'Drotin DS'),

            # === ANTACIDS / ANTI-ULCER ===
            ('Sucrafil O', 'Sucralfate+Oxetacaine', 'Cipla', 'Suspension', 'Sucrafil'),
            ('Esomeprazole 40', 'Esomeprazole', 'Dr Reddys', 'Capsule', 'Esomeprazole,Neksium'),
            ('Neksium 40', 'Esomeprazole', 'AstraZeneca', 'Tablet', 'Neksium 40'),
            ('Famotidine 20', 'Famotidine', 'Sun Pharma', 'Tablet', 'Famotidine'),

            # === ANTI-GOUT ===
            ('Febuget 40', 'Febuxostat', 'Sun Pharma', 'Tablet', 'Febuget,Febuxostat'),
            ('Allopurinol 100', 'Allopurinol', 'Zydus', 'Tablet', 'Allopurinol,Zyloric'),
            ('Zyloric 100', 'Allopurinol', 'GSK', 'Tablet', 'Zyloric 100'),
            ('Colchicine 0.5', 'Colchicine', 'IPCA', 'Tablet', 'Colchicine'),

            # === HORMONAL / GYNAECOLOGICAL ===
            ('Duphaston 10', 'Dydrogesterone', 'Abbott', 'Tablet', 'Duphaston'),
            ('Susten 200', 'Progesterone', 'Sun Pharma', 'Capsule', 'Susten'),
            ('Mala D', 'Ethinyl Estradiol+Levonorgestrel', 'INGA', 'Tablet', 'Mala D'),
            ('Novelon', 'Desogestrel+Ethinyl Estradiol', 'Organon', 'Tablet', 'Novelon'),
            ('Unwanted 72', 'Levonorgestrel', 'Mankind', 'Tablet', 'Unwanted 72'),
            ('iPill', 'Levonorgestrel', 'Piramal', 'Tablet', 'iPill'),
            ('Primolut N', 'Norethisterone', 'Bayer', 'Tablet', 'Primolut'),

            # === ANTI-EMETICS ===
            ('Vomistop 10', 'Domperidone', 'Cipla', 'Tablet', 'Vomistop'),
            ('Ondem 4', 'Ondansetron', 'Alkem', 'Tablet', 'Ondem'),

            # === ANTI-SPASMODICS ===
            ('Buscopan', 'Hyoscine Butylbromide', 'Boehringer Ingelheim', 'Tablet', 'Buscopan'),
            ('Colicaid', 'Simethicone+Dicyclomine', 'Meyer', 'Drop', 'Colicaid'),

            # === ANTI-ANXIETY / SLEEP ===
            ('Restyl 0.25', 'Alprazolam', 'Sun Pharma', 'Tablet', 'Restyl,Alprazolam'),
            ('Alprax 0.5', 'Alprazolam', 'Torrent', 'Tablet', 'Alprax'),
            ('Zolpidem 10', 'Zolpidem', 'Sun Pharma', 'Tablet', 'Zolpidem,Stilnox'),
            ('Nitrest 10', 'Zolpidem', 'Sun Pharma', 'Tablet', 'Nitrest'),

            # === MISCELLANEOUS ===
            ('Tab Ivermectin 12', 'Ivermectin', 'Mankind', 'Tablet', 'Ivermectin'),
            ('Albendazole 400', 'Albendazole', 'GSK', 'Tablet', 'Albendazole,Zentel'),
            ('Zentel 400', 'Albendazole', 'GSK', 'Tablet', 'Zentel 400'),
            ('Mebendazole 100', 'Mebendazole', 'Johnson & Johnson', 'Tablet', 'Mebendazole'),
            ('Disulfiram 250', 'Disulfiram', 'Intas', 'Tablet', 'Disulfiram'),
            ('Pentasa 500', 'Mesalamine', 'Sun Pharma', 'Tablet', 'Pentasa,Mesalamine'),
            ('Ursocol 300', 'Ursodeoxycholic Acid', 'Sun Pharma', 'Tablet', 'Ursocol,UDCA'),
            ('Hepamerz', 'L-Ornithine L-Aspartate', 'Merz', 'Sachet', 'Hepamerz'),
            ('Udiliv 300', 'Ursodeoxycholic Acid', 'Abbott', 'Tablet', 'Udiliv'),
            ('Liv 52', 'Herbal Hepatoprotective', 'Himalaya', 'Tablet', 'Liv 52'),
            ('Silymarin 140', 'Silymarin', 'Micro Labs', 'Tablet', 'Silymarin'),
            ('Domperidone 10', 'Domperidone', 'Sun Pharma', 'Tablet', 'Domperidone'),
            ('Itopride 150', 'Itopride', 'Abbott', 'Tablet', 'Itopride,Ganaton'),
            ('Ganaton 150', 'Itopride', 'Eisai', 'Tablet', 'Ganaton 150'),
            ('Trental 400', 'Pentoxifylline', 'Sanofi', 'Tablet', 'Trental'),
            ('Cilostazol 100', 'Cilostazol', 'Sun Pharma', 'Tablet', 'Cilostazol'),
            ('Nicardia Retard 20', 'Nifedipine', 'J&J', 'Tablet', 'Nicardia,Nifedipine'),
            ('Vertin 16', 'Betahistine', 'Abbott', 'Tablet', 'Vertin,Betahistine'),
            ('Stugeron 25', 'Cinnarizine', 'Johnson & Johnson', 'Tablet', 'Stugeron,Cinnarizine'),
            ('Cetrizine DT', 'Cetirizine', 'Mankind', 'Tablet', 'Cetirizine DT'),
            ('Panderm NM', 'Miconazole+Mometasone+Nadifloxacin', 'Macleods', 'Cream', 'Panderm NM'),
        ]

        conn.executemany(
            '''INSERT INTO medicines (medicine_name, generic_name, company_name, dosage_form, aliases)
               VALUES (?, ?, ?, ?, ?)''',
            medicines
        )


# Auto-initialize and seed the database on import
try:
    init_db()
    seed_medicines()
except Exception:
    pass


def get_all_medicines() -> list:
    """Return all medicines as a list of dicts."""
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM medicines').fetchall()
        return [dict(row) for row in rows]


def search_medicines(query: str) -> list:
    """Search medicines by name or generic name."""
    with get_db() as conn:
        rows = conn.execute(
            '''SELECT * FROM medicines
               WHERE medicine_name LIKE ? OR generic_name LIKE ? OR aliases LIKE ?''',
            (f'%{query}%', f'%{query}%', f'%{query}%')
        ).fetchall()
        return [dict(row) for row in rows]


def save_correction(ocr_text: str, system_guess: str, user_correction: str, confidence: float):
    """Save a user correction to the corrections table."""
    with get_db() as conn:
        conn.execute(
            '''INSERT INTO corrections (ocr_text, system_guess, user_correction, confidence)
               VALUES (?, ?, ?, ?)''',
            (ocr_text, system_guess, user_correction, confidence)
        )


def get_corrections() -> list:
    """Return all corrections as a list of dicts."""
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM corrections ORDER BY created_at DESC').fetchall()
        return [dict(row) for row in rows]
