import { useState } from 'react';
import {
  Sparkles,
  AlertTriangle,
  Scan,
  Send,
  Zap,
  Database,
  Brain,
  UploadCloud,
} from 'lucide-react';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import MedicineCard from '../components/MedicineCard';
import HeroSection from '../components/HeroSection';
import { uploadPrescription } from '../services/api';

export default function HomePage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await uploadPrescription(file);
      setResults(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Failed to analyze prescription. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = () => {
    setFile(null);
    setResults(null);
    setError(null);
  };

  return (
    <>
      {/* Full-screen Hero Landing */}
      <HeroSection />

      {/* Main App Content */}
      <div id="app-content" className="app-content-section">
        <div className="container container-sm">

          {/* Section Header */}
          <div className="page-hero-banner animate-fade-in">
            <div className="page-icon">
              <Scan size={28} />
            </div>
            <h1 className="page-hero-title">
              <span className="gradient-text">Analyze Prescription</span>
            </h1>
            <p className="page-hero-subtitle">
              Upload a handwritten prescription image and our AI will extract
              medicine names and match them to our verified database.
            </p>
          </div>

          {/* Disclaimer */}
          <div className="disclaimer-banner animate-slide-up stagger-2">
            <AlertTriangle className="disclaimer-banner-icon" size={20} />
            <p>
              <strong>Disclaimer:</strong> This tool is for informational and
              educational purposes only. It is <strong>NOT</strong> a substitute
              for professional medical advice, diagnosis, or treatment. Always
              consult a qualified healthcare provider.
            </p>
          </div>

          {/* Upload */}
          <div className="animate-slide-up stagger-3">
            <FileUpload
              file={file}
              onFileSelect={setFile}
              onRemove={handleRemove}
            />
          </div>

          {/* Analyze Button */}
          {file && !loading && !results && (
            <div className="text-center mt-xl animate-scale-in">
              <button
                className="btn-primary btn-lg"
                onClick={handleAnalyze}
                disabled={!file}
              >
                <Scan size={20} />
                <span>Analyze Prescription</span>
                <Send size={16} />
              </button>
            </div>
          )}

          {/* Loading */}
          {loading && <LoadingSpinner />}

          {/* Error */}
          {error && (
            <div className="error-box mt-xl animate-fade-in">
              <AlertTriangle className="error-box-icon" size={20} />
              <p>{error}</p>
            </div>
          )}

          {/* Results */}
          {results && !loading && (
            <div className="mt-2xl animate-fade-in">
              {/* Raw OCR Output */}
              {results.ocr_texts && results.ocr_texts.length > 0 && (
                <section className="mb-xl animate-slide-up stagger-1">
                  <h2 className="section-title">
                    <Scan size={20} />
                    Raw OCR Output
                  </h2>
                  <div className="glass-card-static">
                    <div className="ocr-tokens">
                      {results.ocr_texts.map((token, i) => (
                        <span className="ocr-token" key={i}>
                          {token}
                        </span>
                      ))}
                    </div>
                  </div>
                </section>
              )}

              {/* Matched Medicines */}
              {results.matches && results.matches.length > 0 && (
                <section className="mb-xl animate-slide-up stagger-2">
                  <h2 className="section-title">
                    <Sparkles size={20} />
                    Matched Medicines
                  </h2>
                  <div className="grid grid-2">
                    {results.matches.map((match, i) => (
                      <MedicineCard key={i} match={match} index={i} />
                    ))}
                  </div>
                </section>
              )}

              {/* No Matches */}
              {results.matches && results.matches.length === 0 && (
                <section className="mb-xl">
                  <div className="glass-card text-center">
                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>
                      {results.message || 'No medicine matches found. Try uploading a clearer image.'}
                    </p>
                  </div>
                </section>
              )}

              {/* OCR Engine Status */}
              {results.ocr_status && (
                <section className="mb-xl animate-slide-up stagger-3">
                  <h2 className="section-title">
                    <Zap size={20} />
                    OCR Engine Status
                  </h2>
                  <div className="ocr-status-list">
                    {Object.entries(results.ocr_status).map(
                      ([engine, active]) => (
                        <div
                          className={`ocr-status-item ${active ? 'active' : 'inactive'}`}
                          key={engine}
                        >
                          <span className="ocr-status-dot" />
                          {engine}
                        </div>
                      )
                    )}
                  </div>
                </section>
              )}

              {/* Try Again */}
              <div className="text-center mt-xl animate-fade-in stagger-4">
                <button className="btn-secondary" onClick={handleRemove}>
                  Analyze Another Prescription
                </button>
              </div>
            </div>
          )}

          {/* Feature Highlights */}
          <section id="features" className="mt-2xl">
            <div className="grid grid-3">
              <div className="glass-card animate-slide-up stagger-5">
                <div className="feature-card-icon blue">
                  <Brain size={24} />
                </div>
                <h3 className="feature-card-title">AI-Powered OCR</h3>
                <p className="feature-card-desc">
                  Multi-engine OCR pipeline with Tesseract, EasyOCR, and Google
                  Vision for maximum accuracy on handwritten prescriptions.
                </p>
              </div>

              <div className="glass-card animate-slide-up stagger-6">
                <div className="feature-card-icon cyan">
                  <Database size={24} />
                </div>
                <h3 className="feature-card-title">200+ Medicines</h3>
                <p className="feature-card-desc">
                  Comprehensive database of Indian medicines with generic names,
                  companies, dosage forms, and common aliases.
                </p>
              </div>

              <div className="glass-card animate-slide-up stagger-7">
                <div className="feature-card-icon emerald">
                  <Sparkles size={24} />
                </div>
                <h3 className="feature-card-title">Smart Matching</h3>
                <p className="feature-card-desc">
                  Fuzzy matching algorithm with confidence scoring to find the
                  closest medicine match, even with misspellings.
                </p>
              </div>
            </div>
          </section>

        </div>
      </div>
    </>
  );
}
