import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, BookOpen, MapPin } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/medicines', label: 'Medicine Directory', icon: BookOpen },
    { to: '/pharmacies', label: 'Find Pharmacy', icon: MapPin },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand" onClick={() => setMenuOpen(false)}>
          <span className="navbar-brand-icon">💊</span>
          <span className="gradient-text">RxVision AI</span>
        </Link>

        <button
          className={`navbar-hamburger ${menuOpen ? 'open' : ''}`}
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
        >
          <span />
          <span />
          <span />
        </button>

        <ul className={`navbar-links ${menuOpen ? 'open' : ''}`}>
          {links.map(({ to, label, icon: Icon }) => (
            <li key={to}>
              <Link
                to={to}
                className={`navbar-link ${isActive(to) ? 'active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                <Icon size={16} />
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
