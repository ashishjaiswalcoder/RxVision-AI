import os
from PIL import Image, ImageDraw, PngImagePlugin

# Create directory for sample prescriptions
os.makedirs("sample_prescriptions", exist_ok=True)

samples = [
    {
        "filename": "rx_dolo_azithral_pan.png",
        "medicines": ["Dolo 650", "Azithral 500", "Pan 40"],
        "doctor": "Dr. Sarah Jenkins, MD",
        "specialty": "General Physician",
        "date": "2026-07-17",
    },
    {
        "filename": "rx_crocin_allegra_shelcal.png",
        "medicines": ["Crocin 500mg", "Allegra 120", "Shelcal 500"],
        "doctor": "Dr. Raj Patel, MD",
        "specialty": "Pediatrician & Dermatologist",
        "date": "2026-07-17",
    },
    {
        "filename": "rx_telma_ecosprin_metrogyl.png",
        "medicines": ["Telma 40", "Ecosprin 75", "Metrogyl 400"],
        "doctor": "Dr. Michael Chang, FACC",
        "specialty": "Cardiologist",
        "date": "2026-07-17",
    }
]

for sample in samples:
    # Create a white canvas (simulating paper)
    width, height = 600, 800
    img = Image.new("RGB", (width, height), color="#F7F9FA")
    draw = ImageDraw.Draw(img)

    # Draw border
    draw.rectangle([10, 10, width - 10, height - 10], outline="#1A365D", width=3)
    draw.rectangle([15, 15, width - 15, height - 15], outline="#E2E8F0", width=1)

    # Doctor Header
    draw.text((40, 40), sample["doctor"], fill="#1A365D")
    draw.text((40, 60), sample["specialty"], fill="#4A5568")
    draw.text((40, 80), "Reg No: MC-99482-A", fill="#718096")
    draw.text((400, 40), f"Date: {sample['date']}", fill="#4A5568")

    # Header divider
    draw.line([30, 110, width - 30, 110], fill="#1A365D", width=2)

    # Rx Symbol
    draw.text((40, 140), "Rx", fill="#2B6CB0")

    # Patient Details Placeholder
    draw.text((40, 180), "Patient Name: John Doe", fill="#2D3748")
    draw.text((40, 200), "Age/Gender: 45 / Male", fill="#2D3748")
    draw.line([30, 230, width - 30, 230], fill="#CBD5E0", width=1)

    # Medicines List
    y_offset = 280
    for med in sample["medicines"]:
        # Draw checkmark/bullet
        draw.text((60, y_offset), "->", fill="#319795")
        draw.text((90, y_offset), med, fill="#1A202C")
        draw.text((90, y_offset + 25), "  Sig: 1 tablet daily or as directed", fill="#718096")
        y_offset += 70

    # Footer
    draw.line([30, height - 120, width - 30, height - 120], fill="#CBD5E0", width=1)
    draw.text((40, height - 100), "RxVision AI Verified Prescription", fill="#319795")
    draw.text((40, height - 80), "For educational & demo purposes only.", fill="#A0AEC0")

    # Embed metadata
    meta = PngImagePlugin.PngInfo()
    meds_str = ", ".join(sample["medicines"])
    meta.add_text("prescription_text", meds_str)

    output_path = os.path.join("sample_prescriptions", sample["filename"])
    img.save(output_path, "PNG", pnginfo=meta)
    print(f"Generated {output_path} with metadata: {meds_str}")
