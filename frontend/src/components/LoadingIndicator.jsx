import React from 'react';
import { Bot } from 'lucide-react';

export default function LoadingIndicator() {
  return (
    <div className="message-row agent">
      <div className="message-avatar avatar-agent">
        <Bot size={20} />
      </div>
      <div className="message-content" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem 1rem' }}>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Interviewer is evaluating response...</span>
        <div style={{ display: 'flex', gap: '4px' }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-primary)', animation: 'pulse 1s infinite 0s' }}></span>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-secondary)', animation: 'pulse 1s infinite 0.2s' }}></span>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-cyan)', animation: 'pulse 1s infinite 0.4s' }}></span>
        </div>
      </div>
    </div>
  );
}
