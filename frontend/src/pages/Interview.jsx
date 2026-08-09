import React, { useState, useEffect } from 'react';
import InterviewHeader from '../components/InterviewHeader';
import InterviewChat from '../components/InterviewChat';
import FeedbackPanel from '../components/FeedbackPanel';
import ProgressBar from '../components/ProgressBar';
import { startInterview, sendCandidateTurn } from '../services/api';
import { User, BookOpen, Activity, ShieldCheck } from 'lucide-react';

export default function Interview({ candidate, onReset }) {
  const [sessionId] = useState(() => `session-${Date.now()}`);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [feedback, setFeedback] = useState(null);
  
  // Backend metadata state (initialized from backend API)
  const [questionCount, setQuestionCount] = useState(1);
  const [minQuestions, setMinQuestions] = useState(8);
  const [stage, setStage] = useState('BASELINE');
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [topicsCovered, setTopicsCovered] = useState([]);
  const [daysCovered, setDaysCovered] = useState([]);
  const [currentTopic, setCurrentTopic] = useState('');
  const [error, setError] = useState(null);

  // Initialize interview on mount
  useEffect(() => {
    async function init() {
      if (!candidate) return;
      setLoading(true);
      setError(null);
      try {
        const res = await startInterview(sessionId, candidate);
        setMessages([
          {
            sender: 'agent',
            text: res.reply,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
        
        // Sync state strictly from backend response metadata
        if (res.stage) setStage(res.stage);
        if (res.questionNumber !== undefined) setQuestionCount(res.questionNumber);
        if (res.minQuestions !== undefined) setMinQuestions(res.minQuestions);
        if (res.difficulty) setDifficulty(res.difficulty);
        if (res.topicsCovered) setTopicsCovered(res.topicsCovered);
        if (res.daysCovered) setDaysCovered(res.daysCovered);
        if (res.currentTopic) setCurrentTopic(res.currentTopic);

        if (res.done) {
          setCompleted(true);
          setFeedback(res.feedback);
        }
      } catch (err) {
        console.error('Interview start error:', err);
        setError(err.message || 'Failed to connect to backend AI agent.');
      } finally {
        setLoading(false);
      }
    }
    init();
  }, [candidate, sessionId]);

  const handleSendMessage = async (text) => {
    if (!text.trim() || loading || completed) return;

    const userMsg = {
      sender: 'user',
      text: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await sendCandidateTurn(sessionId, text.trim());
      
      // Update backend metadata state strictly from API response
      if (res.stage) setStage(res.stage);
      if (res.questionNumber !== undefined) setQuestionCount(res.questionNumber);
      if (res.minQuestions !== undefined) setMinQuestions(res.minQuestions);
      if (res.difficulty) setDifficulty(res.difficulty);
      if (res.topicsCovered) setTopicsCovered(res.topicsCovered);
      if (res.daysCovered) setDaysCovered(res.daysCovered);
      if (res.currentTopic) setCurrentTopic(res.currentTopic);

      if (res.done) {
        setCompleted(true);
        setFeedback(res.feedback);
        setMessages(prev => [
          ...prev,
          {
            sender: 'agent',
            text: res.reply || 'Interview completed.',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      } else {
        setMessages(prev => [
          ...prev,
          {
            sender: 'agent',
            text: res.reply,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      }
    } catch (err) {
      console.error('Send message error:', err);
      setError(err.message || 'Failed to send message.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <InterviewHeader
        candidate={candidate}
        stage={stage}
        questionCount={questionCount}
        onReset={onReset}
      />

      <div className="interview-layout">
        {/* Sidebar */}
        <aside className="interview-sidebar">
          <div className="sidebar-card">
            <div className="sidebar-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <User size={16} /> Candidate Profile
            </div>
            <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)' }}>{candidate.member.name}</h3>
            <div style={{ color: 'var(--accent-cyan)', fontSize: '0.875rem', fontWeight: 500, marginBottom: '0.5rem' }}>
              {candidate.member.jobRole}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              {candidate.member.yearsExperience} Years Experience | {candidate.member.education}
            </div>
          </div>

          <div className="sidebar-card">
            <div className="sidebar-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Activity size={16} /> Interview State & Progress
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <span className="stage-badge">{stage}</span>
              <span className="pill" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', borderColor: 'rgba(245, 158, 11, 0.3)' }}>
                {difficulty}
              </span>
            </div>
            <ProgressBar questionCount={questionCount} minQuestions={minQuestions} />
          </div>

          <div className="sidebar-card">
            <div className="sidebar-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <BookOpen size={16} /> Curriculum Assessed
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)', fontWeight: 600, marginBottom: '0.5rem' }}>
              Cohort Days Covered: <span style={{ color: 'var(--accent-cyan)' }}>{daysCovered.length} / 31</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.5rem' }}>
              {topicsCovered.map((topic, idx) => (
                <span key={idx} className="pill" style={{ fontSize: '0.75rem', background: 'rgba(99, 102, 241, 0.15)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                  {topic}
                </span>
              ))}
            </div>
          </div>
        </aside>

        {/* Main Content Workspace */}
        <main style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
          {error && (
            <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.2)', border: '1px solid var(--status-error)', color: '#fca5a5', margin: '1rem' }}>
              ⚠️ Error: {error}
            </div>
          )}

          <InterviewChat
            messages={messages}
            loading={loading}
            onSendMessage={handleSendMessage}
            disabled={completed}
          />

          {completed && feedback && (
            <FeedbackPanel
              feedback={feedback}
              candidate={candidate}
              topicsCovered={topicsCovered}
              daysCovered={daysCovered}
              questionCount={questionCount}
              difficulty={difficulty}
              onRestart={onReset}
            />
          )}
        </main>
      </div>
    </div>
  );
}
