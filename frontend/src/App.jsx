import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import MedicineDirectoryPage from './pages/MedicineDirectoryPage';
import PharmacyFinderPage from './pages/PharmacyFinderPage';

function AppLayout() {
  const location = useLocation();
  const isHome = location.pathname === '/';

  return (
    <>
      {/* Show shared navbar only on sub-pages (hero has its own) */}
      {!isHome && <Navbar />}

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/medicines" element={<MedicineDirectoryPage />} />
        <Route path="/pharmacies" element={<PharmacyFinderPage />} />
      </Routes>

      {/* Footer on all pages */}
      <footer className="footer">
        <div className="footer-inner">
          <p className="footer-disclaimer">
            ⚕️ RxVision AI is an educational tool and does <strong>NOT</strong>{' '}
            provide medical advice. Always consult a licensed healthcare
            professional before taking any medication. Prescription analysis
            results may be inaccurate.
          </p>
          <p className="footer-credits">
            Built with ❤️ using React, Vite &amp; AI — RxVision AI ©{' '}
            {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}
