import { useState } from 'react';
import {
  MapPin,
  Navigation,
  Star,
  Clock,
  Locate,
  AlertCircle,
  Route,
} from 'lucide-react';
import { getPharmacies } from '../services/api';

export default function PharmacyFinderPage() {
  const [pharmacies, setPharmacies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searched, setSearched] = useState(false);

  const handleFind = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      return;
    }

    setLoading(true);
    setError(null);
    setPharmacies([]);
    setSearched(false);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const data = await getPharmacies(pos.coords.latitude, pos.coords.longitude);
          const list = Array.isArray(data) ? data : data.pharmacies || [];
          setPharmacies(list);
          setSearched(true);
        } catch (err) {
          setError(
            err.response?.data?.detail ||
              'Failed to fetch nearby pharmacies. Please try again.'
          );
        } finally {
          setLoading(false);
        }
      },
      (geoErr) => {
        setLoading(false);
        switch (geoErr.code) {
          case geoErr.PERMISSION_DENIED:
            setError(
              'Location access was denied. Please enable location permissions in your browser settings and try again.'
            );
            break;
          case geoErr.POSITION_UNAVAILABLE:
            setError('Location information is unavailable.');
            break;
          case geoErr.TIMEOUT:
            setError('The request to get your location timed out.');
            break;
          default:
            setError('An unknown error occurred while getting your location.');
        }
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const renderStars = (rating) => {
    const stars = [];
    const full = Math.floor(rating || 0);
    for (let i = 0; i < 5; i++) {
      stars.push(
        <Star
          key={i}
          size={14}
          fill={i < full ? '#f59e0b' : 'transparent'}
          stroke={i < full ? '#f59e0b' : 'var(--text-muted)'}
        />
      );
    }
    return stars;
  };

  const formatDistance = (meters) => {
    if (!meters && meters !== 0) return null;
    if (meters < 1000) return `${Math.round(meters)}m`;
    return `${(meters / 1000).toFixed(1)}km`;
  };

  return (
    <div className="page-wrapper page-enter">
      <div className="container" style={{ maxWidth: 900 }}>
        {/* Page Hero Banner */}
        <div className="page-hero-banner animate-fade-in">
          <div className="page-icon">
            <MapPin size={28} />
          </div>
          <h1 className="page-hero-title">
            <span className="gradient-text">Find Nearby Pharmacies</span>
          </h1>
          <p className="page-hero-subtitle">
            Locate pharmacies near you with real-time ratings,
            distances, and open/closed status powered by Google Maps.
          </p>
        </div>

        {/* Find Button */}
        <div className="text-center mb-xl animate-slide-up stagger-2">
          <button
            className="btn-primary btn-lg"
            onClick={handleFind}
            disabled={loading}
          >
            <Locate size={20} />
            <span>{loading ? 'Locating…' : 'Find Nearby Pharmacies'}</span>
          </button>
        </div>

        {/* Loading */}
        {loading && (
          <div className="loading-container">
            <div className="loading-ring" />
            <p className="loading-text">Finding pharmacies near you…</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            className="error-box animate-fade-in"
            style={{ maxWidth: 550, margin: '0 auto' }}
          >
            <AlertCircle className="error-box-icon" size={20} />
            <p>{error}</p>
          </div>
        )}

        {/* Results */}
        {!loading && pharmacies.length > 0 && (
          <div className="animate-fade-in">
            <p className="results-count text-center">
              Found <span>{pharmacies.length}</span> pharmacies nearby
            </p>

            <div className="grid grid-2">
              {pharmacies.map((pharmacy, i) => (
                <div
                  key={pharmacy.place_id || i}
                  className="glass-card medicine-card animate-scale-in"
                  style={{ animationDelay: `${i * 0.06}s` }}
                >
                  <div className="pharmacy-card-header">
                    <div>
                      <h3 className="pharmacy-card-name">{pharmacy.name}</h3>
                      {pharmacy.address && (
                        <p className="pharmacy-card-address">
                          <MapPin
                            size={13}
                            style={{
                              display: 'inline',
                              verticalAlign: 'middle',
                              marginRight: 4,
                            }}
                          />
                          {pharmacy.address}
                        </p>
                      )}
                    </div>
                    <span
                      className={`status-badge ${pharmacy.open_now ? 'open' : 'closed'}`}
                    >
                      <Clock size={12} />
                      {pharmacy.open_now ? 'Open' : 'Closed'}
                    </span>
                  </div>

                  <div className="pharmacy-card-meta">
                    {pharmacy.rating != null && (
                      <div className="pharmacy-card-rating">
                        {renderStars(pharmacy.rating)}
                        <span style={{ marginLeft: 4 }}>{pharmacy.rating}</span>
                      </div>
                    )}

                    {pharmacy.distance != null && (
                      <div className="pharmacy-card-distance">
                        <Route size={14} />
                        {formatDistance(pharmacy.distance)}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty after search */}
        {!loading && searched && pharmacies.length === 0 && !error && (
          <div className="empty-state animate-fade-in">
            <Navigation className="empty-state-icon" size={56} />
            <h3 className="empty-state-title">No pharmacies found nearby</h3>
            <p className="empty-state-desc">
              Try increasing the search radius or check back later.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
