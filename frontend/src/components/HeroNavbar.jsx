import { Link } from 'react-router-dom';
import { ChevronDown } from 'lucide-react';

export default function HeroNavbar() {
  return (
    <nav className="hero-nav">
      <div className="hero-nav-inner">
        {/* Left: Logo */}
        <Link to="/" className="hero-nav-logo">
          <span className="hero-nav-logo-icon">💊</span>
          <span className="hero-nav-logo-text">RxVision AI</span>
        </Link>

        {/* Center: Nav Items */}
        <div className="hero-nav-links">
          <a href="#app-content" className="hero-nav-link">
            Scan Prescription
          </a>
          <Link to="/medicines" className="hero-nav-link">
            Medicine Directory
          </Link>
          <Link to="/pharmacies" className="hero-nav-link">
            Find Pharmacy
          </Link>
          <a href="#features" className="hero-nav-link">
            Features
            <ChevronDown size={14} />
          </a>
        </div>

        {/* Right: CTA */}
        <a href="#app-content" className="hero-nav-cta">
          Try It Free
        </a>
      </div>

      {/* Gradient Divider */}
      <div className="hero-nav-divider" />
    </nav>
  );
}
