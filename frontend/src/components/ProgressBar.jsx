import React from 'react';

export default function ProgressBar({ questionCount, minQuestions = 8, stage = 'BASELINE' }) {
  const percent = Math.min(100, Math.round((questionCount / minQuestions) * 100));

  return (
    <div style={{ width: '100%', marginBottom: '0.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
        <span>Question Progress: <strong>{questionCount}</strong> / min {minQuestions}</span>
        <span>{percent}%</span>
      </div>
      <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '999px', overflow: 'hidden' }}>
        <div 
          style={{ 
            height: '100%', 
            width: `${percent}%`, 
            background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-cyan))',
            transition: 'width 0.4s ease'
          }} 
        />
      </div>
    </div>
  );
}
