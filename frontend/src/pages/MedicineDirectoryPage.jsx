import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, PackageSearch, BookOpen } from 'lucide-react';
import MedicineCard from '../components/MedicineCard';
import { getMedicines } from '../services/api';

const CATEGORIES = [
  'All',
  'Tablet',
  'Capsule',
  'Syrup',
  'Injection',
  'Cream',
  'Drops',
  'Inhaler',
  'Ointment',
  'Powder',
  'Gel',
];

export default function MedicineDirectoryPage() {
  const [medicines, setMedicines] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const debounceRef = useRef(null);

  // Fetch all medicines on mount
  useEffect(() => {
    (async () => {
      try {
        const data = await getMedicines();
        const list = Array.isArray(data) ? data : data.medicines || [];
        setMedicines(list);
        setFiltered(list);
      } catch (err) {
        setError('Failed to load medicine directory. Is the API running?');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  // Filter logic
  const applyFilters = useCallback(
    (q, cat) => {
      let list = medicines;

      if (cat !== 'All') {
        list = list.filter(
          (m) =>
            m.dosage_form &&
            m.dosage_form.toLowerCase().includes(cat.toLowerCase())
        );
      }

      if (q.trim()) {
        const lower = q.toLowerCase();
        list = list.filter(
          (m) =>
            m.medicine_name?.toLowerCase().includes(lower) ||
            m.generic_name?.toLowerCase().includes(lower) ||
            m.company_name?.toLowerCase().includes(lower) ||
            (m.aliases && m.aliases.toLowerCase().includes(lower))
        );
      }

      setFiltered(list);
    },
    [medicines]
  );

  // Debounced search
  const handleSearch = (value) => {
    setQuery(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      applyFilters(value, category);
    }, 300);
  };

  const handleCategory = (cat) => {
    setCategory(cat);
    applyFilters(query, cat);
  };

  return (
    <div className="page-wrapper page-enter">
      <div className="container">
        {/* Page Hero Banner */}
        <div className="page-hero-banner animate-fade-in">
          <div className="page-icon">
            <BookOpen size={28} />
          </div>
          <h1 className="page-hero-title">
            <span className="gradient-text">Medicine Directory</span>
          </h1>
          <p className="page-hero-subtitle">
            Browse and search our comprehensive database of 200+ verified medicines
            with generic names, dosage forms, and manufacturer details.
          </p>
        </div>

        {/* Search */}
        <div
          className="input-with-icon animate-slide-up stagger-2"
          style={{ maxWidth: 520, margin: '0 auto var(--space-lg)' }}
        >
          <Search className="input-icon" size={18} />
          <input
            className="input"
            type="text"
            placeholder="Search by name, generic, company…"
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
          />
        </div>

        {/* Category Chips */}
        <div
          className="filter-chips animate-slide-up stagger-3"
          style={{ justifyContent: 'center' }}
        >
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              className={`filter-chip ${category === cat ? 'active' : ''}`}
              onClick={() => handleCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Results Count */}
        {!loading && !error && (
          <p className="results-count text-center animate-fade-in stagger-4">
            Showing <span>{filtered.length}</span> of{' '}
            <span>{medicines.length}</span> medicines
          </p>
        )}

        {/* Loading */}
        {loading && (
          <div className="loading-container">
            <div className="loading-ring" />
            <p className="loading-text">Loading medicines…</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            className="error-box animate-fade-in"
            style={{ maxWidth: 500, margin: '0 auto' }}
          >
            <PackageSearch
              size={20}
              style={{ color: 'var(--confidence-low)', flexShrink: 0 }}
            />
            <p>{error}</p>
          </div>
        )}

        {/* Grid */}
        {!loading && !error && filtered.length > 0 && (
          <div className="grid grid-3 animate-fade-in stagger-5">
            {filtered.map((med, i) => (
              <MedicineCard
                key={med.medicine_name || med.id || i}
                medicine={med}
                index={i}
              />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && filtered.length === 0 && (
          <div className="empty-state animate-fade-in">
            <PackageSearch className="empty-state-icon" size={56} />
            <h3 className="empty-state-title">No medicines found</h3>
            <p className="empty-state-desc">
              Try adjusting your search or category filter.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
