/**
 * API service helper for the AI Interview Agent backend endpoints.
 */

const API_BASE = '/api';

export async function fetchCandidates() {
  const res = await fetch(`${API_BASE}/candidates`);
  if (!res.ok) {
    throw new Error('Failed to fetch candidate profiles.');
  }
  const data = await res.json();
  return data.candidates || [];
}

export async function fetchCurriculum() {
  const res = await fetch(`${API_BASE}/curriculum`);
  if (!res.ok) {
    throw new Error('Failed to fetch curriculum.');
  }
  return await res.json();
}

export async function startInterview(sessionId, candidateObj) {
  const res = await fetch(`${API_BASE}/interview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sessionId,
      candidate: candidateObj
    })
  });
  
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Failed to start interview.' }));
    throw new Error(errorData.detail || 'Server error starting interview.');
  }
  
  return await res.json();
}

export async function sendCandidateTurn(sessionId, messageText) {
  const res = await fetch(`${API_BASE}/interview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sessionId,
      message: messageText
    })
  });
  
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Failed to process turn.' }));
    throw new Error(errorData.detail || 'Server error processing interview turn.');
  }
  
  return await res.json();
}

export async function fetchSessionInfo(sessionId) {
  const res = await fetch(`${API_BASE}/session/${sessionId}`);
  if (!res.ok) {
    return null;
  }
  return await res.json();
}
