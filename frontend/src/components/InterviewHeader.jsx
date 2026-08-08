import React from 'react';
import { Bot, User, Sparkles, RefreshCw } from 'lucide-react';
import ProgressBar from './ProgressBar';

export default function InterviewHeader({ candidate, stage, questionCount, onReset }) {
  return (
    <header className="app-header">
      <div className="brand-logo">
        <div style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', width: 34, height: 34, borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Bot size={20} color="white" />
        </div>
        <span>AI Interview Agent</span>
        <span className="brand-badge">Adaptive Engine</span>
      </div>

      {candidate && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
            <User size={16} color="var(--accent-cyan)" />
            <strong>{candidate.member.name}</strong>
            <span style={{ color: 'var(--text-muted)' }}>({candidate.member.jobRole})</span>
          </div>

          <button 
            onClick={onReset}
            style={{ 
              background: 'transparent', 
              border: '1px solid var(--border-color)', 
              color: 'var(--text-secondary)',
              padding: '0.35rem 0.75rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.8rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem'
            }}
          >
            <RefreshCw size={14} />
            Reset Session
          </button>
        </div>
      )}
    </header>
  );
}
