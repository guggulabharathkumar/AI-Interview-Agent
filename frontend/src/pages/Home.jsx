import React from 'react';
import CandidateSelector from '../components/CandidateSelector';
import { Bot, Sparkles, Brain, Target, ShieldCheck, Zap } from 'lucide-react';

export default function Home({ candidates, selectedCandidate, onSelectCandidate, onStartInterview }) {
  return (
    <div className="home-page">
      <div className="hero-section">
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(99, 102, 241, 0.15)', border: '1px solid rgba(99, 102, 241, 0.3)', padding: '0.35rem 1rem', borderRadius: 'var(--radius-full)', color: '#a5b4fc', fontSize: '0.85rem', fontWeight: 600, marginBottom: '1.25rem' }}>
          <Sparkles size={16} /> Autonomous Adaptive Technical Interviewer
        </div>
        <h1 className="hero-title">
          Build the interviewer, not the interview.
        </h1>
        <p className="hero-subtitle">
          AI Interview Agent personalizes technical interviews based on candidate learning history, adaptively probes answers with multi-turn follow-ups, and delivers actionable final feedback.
        </p>
      </div>

      <div style={{ marginBottom: '2.5rem' }}>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          Select a Candidate Profile
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
          Choose a candidate from the cohort dataset to launch a personalized technical evaluation:
        </p>

        <CandidateSelector
          candidates={candidates}
          selectedCandidate={selectedCandidate}
          onSelect={onSelectCandidate}
          onStart={onStartInterview}
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem', marginTop: '3rem', paddingTop: '2.5rem', borderTop: '1px solid var(--border-color)' }}>
        <div className="sidebar-card">
          <div style={{ color: 'var(--accent-primary)', marginBottom: '0.5rem' }}><Brain size={24} /></div>
          <h4 style={{ marginBottom: '0.35rem' }}>Candidate Personalization</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Analyzes passed, failed, and skipped missions, commit activity, and experience level to adjust technical depth.
          </p>
        </div>

        <div className="sidebar-card">
          <div style={{ color: 'var(--accent-cyan)', marginBottom: '0.5rem' }}><Target size={24} /></div>
          <h4 style={{ marginBottom: '0.35rem' }}>Adaptive Stage Machine</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Progresses through Baseline, Deep-Dive Probing, Cross-Topic Synthesis, System Design, and Production Reliability.
          </p>
        </div>

        <div className="sidebar-card">
          <div style={{ color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}><Zap size={24} /></div>
          <h4 style={{ marginBottom: '0.35rem' }}>Multi-Turn Follow-Ups</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Evaluates candidate answers in real-time to ask deeper trade-offs, debugging scenarios, or structural clarifications.
          </p>
        </div>

        <div className="sidebar-card">
          <div style={{ color: 'var(--status-success)', marginBottom: '0.5rem' }}><ShieldCheck size={24} /></div>
          <h4 style={{ marginBottom: '0.35rem' }}>Structured Feedback</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Generates standardized report containing summary, strengths, knowledge gaps, and concrete recommended next steps.
          </p>
        </div>
      </div>
    </div>
  );
}
