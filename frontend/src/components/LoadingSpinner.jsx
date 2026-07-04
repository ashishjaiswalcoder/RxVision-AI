import { useState, useEffect } from 'react';
import { Image, ScanText, Search, CheckCircle2, ChevronRight } from 'lucide-react';

const STEPS = [
  { label: 'Image Processing', icon: Image },
  { label: 'OCR Extraction', icon: ScanText },
  { label: 'Medicine Matching', icon: Search },
];

const STEP_DURATION = 3000; // ms per step

export default function LoadingSpinner() {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => {
        if (prev < STEPS.length - 1) return prev + 1;
        return prev; // stay on last step
      });
    }, STEP_DURATION);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-container animate-fade-in">
      <div className="loading-ring" />
      <p className="loading-text">Analyzing prescription…</p>

      <div className="loading-steps">
        {STEPS.map((step, i) => {
          const Icon = step.icon;
          let state = 'pending';
          if (i < activeStep) state = 'done';
          else if (i === activeStep) state = 'active';

          return (
            <div key={step.label} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div className={`loading-step ${state}`}>
                {state === 'done' ? <CheckCircle2 size={14} /> : <Icon size={14} />}
                {step.label}
              </div>
              {i < STEPS.length - 1 && (
                <span className="loading-step-arrow"><ChevronRight size={14} /></span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
