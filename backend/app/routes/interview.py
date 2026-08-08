import logging
from fastapi import APIRouter, HTTPException, status
from app.models import InterviewRequest, InterviewResponse, Candidate
from app.services.interview_service import interview_service
from app.services.session_service import session_service
from app.services.candidate_service import candidate_service
from app.services.curriculum_service import curriculum_service

logger = logging.getLogger("ai_interview_agent.api")
router = APIRouter(prefix="/api", tags=["Interview"])

@router.post("/interview", response_model=InterviewResponse)
async def handle_interview(req: InterviewRequest):
    """Main Interview Endpoint enforcing the required Technical Spec API contract."""
    if not req.sessionId or not req.sessionId.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'sessionId'."
        )

    # Check if this is a START request
    if req.candidate is not None:
        try:
            candidate_dict = req.candidate.model_dump()
            res = await interview_service.start_interview(req.sessionId, candidate_dict)
            return res
        except Exception as e:
            logger.error(f"Error starting interview for session {req.sessionId}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to start interview: {str(e)}"
            )

    # Subsequent Turn request
    if req.message is not None:
        if not req.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Candidate message cannot be empty."
            )
        try:
            res = await interview_service.process_candidate_turn(req.sessionId, req.message)
            return res
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error processing turn for session {req.sessionId}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Interview turn processing error: {str(e)}"
            )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Request must contain either 'candidate' to start or 'message' to continue."
    )

@router.get("/candidates")
def list_candidates():
    """Helper endpoint returning pre-loaded candidates for frontend selection."""
    candidates = candidate_service.get_all_candidates()
    return {"candidates": [c.model_dump() for c in candidates]}

@router.get("/curriculum")
def get_curriculum():
    """Helper endpoint returning full 31-day 8-module curriculum."""
    curr = curriculum_service.get_curriculum()
    return curr.model_dump() if curr else {}

@router.get("/session/{session_id}")
def get_session_info(session_id: str):
    """Helper endpoint returning current active session state."""
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session.model_dump()
