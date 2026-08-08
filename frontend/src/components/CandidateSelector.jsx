import React from 'react';
import { User, Award, CheckCircle2, AlertCircle, HelpCircle, ArrowRight } from 'lucide-react';

export default function CandidateSelector({ candidates, selectedCandidate, onSelect, onStart }) {
  if (!candidates || candidates.length === 0) {
    return <div className="loading">Loading candidates dataset...</div>;
  }

  return (
    <div>
      <div className="candidate-grid">
        {candidates.map((cand) => {
          const isSelected = selectedCandidate?.member?.id === cand.member.id;
          const passedCount = cand.missions.filter(m => m.passed).length;
          const skippedCount = cand.missions.filter(m => m.skipped).length;
          const failedCount = cand.missions.filter(m => !m.passed && !m.skipped).length;

          return (
            <div
              key={cand.member.id}
              className={`candidate-card ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelect(cand)}
            >
              <div className="card-header">
                <div>
                  <h3 className="candidate-name">{cand.member.name}</h3>
                  <div className="candidate-role">{cand.member.jobRole}</div>
                </div>
                <span className="pill">{cand.member.yearsExperience} yrs exp</span>
              </div>

              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                🎓 {cand.member.education}
              </div>

              <div className="stats-pills">
                <span className="pill passed">
                  <CheckCircle2 size={12} style={{ display: 'inline', marginRight: 4 }} />
                  {passedCount} Passed
                </span>
                {failedCount > 0 && (
                  <span className="pill failed">
                    <AlertCircle size={12} style={{ display: 'inline', marginRight: 4 }} />
                    {failedCount} Failed
                  </span>
                )}
                {skippedCount > 0 && (
                  <span className="pill skipped">
                    <HelpCircle size={12} style={{ display: 'inline', marginRight: 4 }} />
                    {skippedCount} Skipped
                  </span>
                )}
                <span className="pill">
                  ⚡ {cand.signals.commitDays} Days Active
                </span>
              </div>

              <div style={{ marginTop: 'auto', paddingTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  ID: {cand.member.id}
                </span>
                <span style={{ fontSize: '0.85rem', color: isSelected ? 'var(--accent-primary)' : 'var(--text-muted)', fontWeight: 600 }}>
                  {isSelected ? '✓ Selected' : 'Click to select'}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {selectedCandidate && (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button className="btn-primary" onClick={onStart}>
            <span>Start Interview for {selectedCandidate.member.name}</span>
            <ArrowRight size={18} />
          </button>
        </div>
      )}
    </div>
  );
}
