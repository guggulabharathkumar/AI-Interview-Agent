import React, { useState, useEffect } from 'react';
import Home from './pages/Home';
import Interview from './pages/Interview';
import { fetchCandidates } from './services/api';

export default function App() {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [activeView, setActiveView] = useState('home'); // 'home' | 'interview'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const list = await fetchCandidates();
        setCandidates(list);
        if (list.length > 0) {
          setSelectedCandidate(list[0]);
        }
      } catch (err) {
        console.error('Error fetching candidates:', err);
        setError('Could not load candidate dataset from backend.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleStartInterview = () => {
    if (selectedCandidate) {
      setActiveView('interview');
    }
  };

  const handleReset = () => {
    setActiveView('home');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
        Loading AI Interview Agent...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ color: 'var(--status-error)', fontSize: '1.2rem' }}>⚠️ {error}</div>
        <p style={{ color: 'var(--text-muted)' }}>Make sure the FastAPI backend is running on port 8000.</p>
        <button onClick={() => window.location.reload()} style={{ padding: '0.5rem 1rem', background: 'var(--accent-primary)', color: 'white', borderRadius: 6 }}>
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div>
      {activeView === 'home' ? (
        <Home
          candidates={candidates}
          selectedCandidate={selectedCandidate}
          onSelectCandidate={setSelectedCandidate}
          onStartInterview={handleStartInterview}
        />
      ) : (
        <Interview
          candidate={selectedCandidate}
          onReset={handleReset}
        />
      )}
    </div>
  );
}
