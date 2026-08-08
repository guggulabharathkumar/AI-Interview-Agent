import logging
from typing import Dict, Any, Tuple
from app.models import (
    Candidate, InterviewResponse, FeedbackResponse,
    SessionState, StageEnum, QuestionMetadata, EvaluationResult
)
from app.services.candidate_service import candidate_service
from app.services.curriculum_service import curriculum_service
from app.services.session_service import session_service
from app.agents.question_planner import question_planner_agent
from app.agents.evaluator import evaluator_agent
from app.agents.interviewer import interviewer_agent
from app.agents.feedback_generator import feedback_generator_agent

logger = logging.getLogger("ai_interview_agent.service")

class InterviewService:
    """Orchestrates adaptive technical interview state machine and agent actions."""

    async def start_interview(self, session_id: str, candidate_data: Dict[str, Any]) -> InterviewResponse:
        logger.info(f"Starting interview session {session_id} for candidate {candidate_data.get('member', {}).get('name')}")
        
        # Parse candidate object
        candidate = Candidate(**candidate_data)
        
        # Analyze candidate profile
        analyzed_profile = candidate_service.analyze_candidate(candidate)
        
        # Create new session
        session = session_service.create_session(
            session_id=session_id,
            candidate=candidate,
            analyzed_profile=analyzed_profile
        )

        # Plan first question
        session.stage = StageEnum.BASELINE
        question_meta = await question_planner_agent.plan_question(session)
        
        session.questions.append(question_meta)
        session.currentTopic = question_meta.topic
        session.currentDay = question_meta.day
        if question_meta.topic not in session.topicsCovered:
            session.topicsCovered.append(question_meta.topic)
        if question_meta.day not in session.daysCovered:
            session.daysCovered.append(question_meta.day)

        # Initial interviewer message
        welcome_reply = f"Welcome {candidate.member.name}. Let's begin your technical interview.\n\nTo start off: {question_meta.question}"
        
        session_service.save_session(session)
        return InterviewResponse(reply=welcome_reply, done=False)

    async def process_candidate_turn(self, session_id: str, candidate_message: str) -> InterviewResponse:
        session = session_service.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found.")

        if session.completed:
            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=session.feedback
            )

        logger.info(f"Session {session_id} - Turn {session.questionCount + 1} - Message len: {len(candidate_message)}")

        # 1. Record candidate answer
        session.answers.append(candidate_message)
        session.questionCount += 1

        # 2. Get last asked question metadata
        current_q_meta = session.questions[-1] if session.questions else QuestionMetadata(
            question="Previous topic", day=7, topic="Embeddings explained",
            difficulty=session.difficulty, type="conceptual", purpose="Baseline assessment"
        )

        # 3. Evaluate answer
        eval_result = await evaluator_agent.evaluate_answer(
            question_meta=current_q_meta,
            candidate_answer=candidate_message,
            candidate_role=session.candidate.member.jobRole
        )
        session.evaluations.append(eval_result)

        # 4. Adapt difficulty based on score
        if eval_result.score >= 8.0:
            if session.difficulty == "Beginner":
                session.difficulty = "Intermediate"
            elif session.difficulty == "Intermediate":
                session.difficulty = "Advanced"
            elif session.difficulty == "Advanced":
                session.difficulty = "System Design"
        elif eval_result.score <= 4.0:
            if session.difficulty == "System Design":
                session.difficulty = "Advanced"
            elif session.difficulty == "Advanced":
                session.difficulty = "Intermediate"
            elif session.difficulty == "Intermediate":
                session.difficulty = "Beginner"

        # 5. Check stage progression and completion criteria
        # Minimum: 8 questions. Maximum: 15 questions. 4+ curriculum days required.
        q_count = session.questionCount
        unique_days_covered = len(set(session.daysCovered))

        should_finish = False
        if q_count >= 15:
            should_finish = True
        elif q_count >= 8 and unique_days_covered >= 4:
            # Reached minimum criteria (8 questions & 4+ days)
            # If performance is decisive, finish now, else extend up to 12
            if eval_result.score >= 7.0 or eval_result.score <= 4.0 or q_count >= 12:
                should_finish = True

        if should_finish:
            session.stage = StageEnum.COMPLETED
            session.completed = True
            
            # Generate final feedback
            feedback = await feedback_generator_agent.generate_feedback(session)
            session.feedback = feedback
            session_service.save_session(session)

            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=feedback
            )

        # Update Stage State Machine
        if q_count < 2:
            session.stage = StageEnum.BASELINE
        elif q_count < 4:
            session.stage = StageEnum.DEEP_DIVE
        elif q_count < 6:
            session.stage = StageEnum.CROSS_TOPIC
        elif q_count < 8:
            session.stage = StageEnum.SYSTEM_DESIGN
        else:
            session.stage = StageEnum.PRODUCTION

        # 6. Plan Next Question / Follow-up
        next_q_meta = await question_planner_agent.plan_question(session)
        session.questions.append(next_q_meta)
        session.currentTopic = next_q_meta.topic
        session.currentDay = next_q_meta.day

        if next_q_meta.topic not in session.topicsCovered:
            session.topicsCovered.append(next_q_meta.topic)
        if next_q_meta.day not in session.daysCovered:
            session.daysCovered.append(next_q_meta.day)

        # 7. Generate realistic Interviewer Reply
        interviewer_reply = await interviewer_agent.generate_response(
            session=session,
            question_meta=next_q_meta,
            candidate_last_answer=candidate_message,
            last_eval=eval_result
        )

        session_service.save_session(session)
        return InterviewResponse(reply=interviewer_reply, done=False)

interview_service = InterviewService()
