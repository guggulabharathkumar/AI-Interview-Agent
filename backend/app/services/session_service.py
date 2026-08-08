import datetime
from typing import Dict, Optional, List
from app.models import Candidate, AnalyzedCandidateProfile, SessionState, StageEnum

class SessionService:
    """Thread-safe in-memory session manager for interview state management."""
    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def create_session(
        self,
        session_id: str,
        candidate: Candidate,
        analyzed_profile: AnalyzedCandidateProfile
    ) -> SessionState:
        now_str = datetime.datetime.utcnow().isoformat()
        session = SessionState(
            sessionId=session_id,
            candidate=candidate,
            analyzedProfile=analyzed_profile,
            stage=StageEnum.INTRO,
            questionCount=0,
            topicsCovered=[],
            daysCovered=[],
            questions=[],
            answers=[],
            evaluations=[],
            currentTopic=None,
            currentDay=None,
            difficulty=analyzed_profile.recommendedDifficulty,
            startedAt=now_str,
            completed=False
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        return self._sessions.get(session_id)

    def save_session(self, session: SessionState) -> SessionState:
        self._sessions[session.sessionId] = session
        return session

    def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def list_sessions(self) -> List[SessionState]:
        return list(self._sessions.values())

session_service = SessionService()
