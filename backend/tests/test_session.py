import pytest
from app.services.session_service import session_service
from app.services.candidate_service import candidate_service

def test_session_lifecycle():
    candidates = candidate_service.get_all_candidates()
    assert len(candidates) > 0
    candidate = candidates[0]
    analyzed = candidate_service.analyze_candidate(candidate)

    session_id = "test-session-999"
    session = session_service.create_session(session_id, candidate, analyzed)
    assert session.sessionId == session_id
    assert session.candidate.member.id == candidate.member.id

    fetched = session_service.get_session(session_id)
    assert fetched is not None
    assert fetched.sessionId == session_id

    session_service.delete_session(session_id)
    assert session_service.get_session(session_id) is None
