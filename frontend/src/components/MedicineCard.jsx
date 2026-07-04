import { Pill, Building2, FlaskConical, FileText, Eye } from 'lucide-react';

const BADGE_CONFIG = {
  HIGH:      { className: 'high',     label: 'High' },
  MEDIUM:    { className: 'medium',   label: 'Medium' },
  LOW:       { className: 'low',      label: 'Low' },
  'VERY LOW':{ className: 'very-low', label: 'Very Low' },
};

export default function MedicineCard({ match, medicine, index = 0 }) {
  // Support both "match" from analysis results and "medicine" from directory
  let name, genericName, company, dosageForm, aliases, ocrText, confidence, confidenceLabel;

  if (match) {
    // From backend /api/upload response
    const info = match.medicine_info || {};
    name = info.medicine_name || match.matched_name;
    genericName = info.generic_name;
    company = info.company_name;
    dosageForm = info.dosage_form;
    aliases = info.aliases;
    ocrText = match.ocr_text;
    confidence = match.confidence;
    confidenceLabel = match.confidence_label;
  } else if (medicine) {
    // From /api/medicines directory listing
    name = medicine.medicine_name || medicine.name;
    genericName = medicine.generic_name;
    company = medicine.company_name || medicine.company;
    dosageForm = medicine.dosage_form;
    aliases = medicine.aliases;
    confidence = medicine.confidence;
    confidenceLabel = medicine.confidence_label;
    ocrText = medicine.ocr_text;
  }

  const badgeCfg = confidenceLabel ? BADGE_CONFIG[confidenceLabel] : null;
  const confPercent = confidence != null ? Math.round(confidence * 100) : null;

  return (
    <div
      className="glass-card medicine-card"
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      <div className="medicine-card-header">
        <h3 className="medicine-card-name">{name}</h3>
        {badgeCfg && confPercent != null && (
          <span className={`confidence-badge ${badgeCfg.className}`}>
            {badgeCfg.label} {confPercent}%
          </span>
        )}
      </div>

      {genericName && (
        <div className="medicine-card-row">
          <Pill size={16} />
          <strong>Generic</strong>
          <span>{genericName}</span>
        </div>
      )}

      {company && (
        <div className="medicine-card-row">
          <Building2 size={16} />
          <strong>Company</strong>
          <span>{company}</span>
        </div>
      )}

      {dosageForm && (
        <div className="medicine-card-row">
          <FlaskConical size={16} />
          <strong>Form</strong>
          <span>{dosageForm}</span>
        </div>
      )}

      {aliases && aliases.length > 0 && (
        <div className="medicine-card-row">
          <FileText size={16} />
          <strong>Aliases</strong>
          <span>{typeof aliases === 'string' ? aliases : aliases.join(', ')}</span>
        </div>
      )}

      {ocrText && (
        <div className="ocr-raw-tag" title="OCR raw text">
          <Eye size={14} />
          {ocrText}
        </div>
      )}
    </div>
  );
}
