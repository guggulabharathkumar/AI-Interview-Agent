import React from 'react';
import { Award, CheckCircle2, AlertTriangle, Lightbulb, RefreshCw, BookOpen, Layers, BarChart2 } from 'lucide-react';

export default function FeedbackPanel({ feedback, candidate, topicsCovered, daysCovered, questionCount, difficulty, onRestart }) {
  if (!feedback) return null;

  return (
    <div className="feedback-dashboard">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <span className="brand-badge" style={{ background: 'var(--status-success)', color: 'white' }}>
            ✓ Technical Assessment Complete
          </span>
          <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.75rem', marginTop: '0.5rem' }}>
            Evidence-Based Feedback Report
          </h2>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Candidate: <strong>{candidate?.member?.name}</strong> | Role: <strong>{candidate?.member?.jobRole}</strong> ({candidate?.member?.yearsExperience} Yrs Exp)
          </div>
        </div>

        <button className="btn-primary" onClick={onRestart}>
          <RefreshCw size={16} />
          Start New Interview
        </button>
      </div>

      {/* Metrics Summary Banner */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div style={{ background: 'rgba(15, 23, 42, 0.7)', border: '1px solid var(--border-color)', padding: '0.85rem 1rem', borderRadius: 'var(--radius-md)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <Layers size={14} /> Total Questions
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '0.2rem' }}>
            {questionCount || 8} Turns
          </div>
        </div>

        <div style={{ background: 'rgba(15, 23, 42, 0.7)', border: '1px solid var(--border-color)', padding: '0.85rem 1rem', borderRadius: 'var(--radius-md)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <BookOpen size={14} /> Cohort Days Covered
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '0.2rem' }}>
            {daysCovered?.length || 4} Days
          </div>
        </div>

        <div style={{ background: 'rgba(15, 23, 42, 0.7)', border: '1px solid var(--border-color)', padding: '0.85rem 1rem', borderRadius: 'var(--radius-md)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <BarChart2 size={14} /> Difficulty Reached
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--status-warning)', marginTop: '0.2rem' }}>
            {difficulty || 'Advanced'}
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid var(--border-highlight)', padding: '1.25rem', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem' }}>
        <div style={{ fontWeight: 600, color: 'var(--accent-cyan)', marginBottom: '0.35rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Award size={18} /> Executive Synthesis
        </div>
        <p style={{ color: 'var(--text-primary)', fontSize: '1rem', lineHeight: '1.6' }}>
          {feedback.summary}
        </p>
      </div>

      {/* Strengths */}
      <div className="feedback-section">
        <h3 className="feedback-section-title" style={{ color: 'var(--status-success)' }}>
          <CheckCircle2 size={20} /> Key Demonstrated Strengths
        </h3>
        <ul className="feedback-list">
          {feedback.strengths.map((item, idx) => (
            <li key={idx} className="feedback-item strength">
              {item}
            </li>
          ))}
        </ul>
      </div>

      {/* Knowledge Gaps */}
      <div className="feedback-section">
        <h3 className="feedback-section-title" style={{ color: 'var(--status-warning)' }}>
          <AlertTriangle size={20} /> Identified Knowledge Gaps
        </h3>
        <ul className="feedback-list">
          {feedback.gaps.map((item, idx) => (
            <li key={idx} className="feedback-item gap">
              {item}
            </li>
          ))}
        </ul>
      </div>

      {/* Recommended Next Steps */}
      <div className="feedback-section">
        <h3 className="feedback-section-title" style={{ color: 'var(--accent-cyan)' }}>
          <Lightbulb size={20} /> Recommended Next Steps
        </h3>
        <ul className="feedback-list">
          {feedback.next.map((item, idx) => (
            <li key={idx} className="feedback-item next">
              {item}
            </li>
          ))}
        </ul>
      </div>

      {/* Topics Covered Chips */}
      {topicsCovered && topicsCovered.length > 0 && (
        <div className="feedback-section" style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <BookOpen size={16} /> Curriculum Modules Assessed:
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {topicsCovered.map((topic, i) => (
              <span key={i} className="pill" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
