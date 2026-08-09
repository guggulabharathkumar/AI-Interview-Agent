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

        # Initial baseline question
        session.stage = StageEnum.BASELINE
        question_meta = await question_planner_agent.plan_question(session)
        
        session.questions.append(question_meta)
        session.currentQuestion = question_meta.model_dump()
        session.currentTopic = question_meta.topic
        session.currentDay = question_meta.day
        if question_meta.topic not in session.topicsCovered:
            session.topicsCovered.append(question_meta.topic)
        if question_meta.day not in session.daysCovered:
            session.daysCovered.append(question_meta.day)

        # Welcome message
        welcome_reply = f"Welcome {candidate.member.name}. Let's begin your technical interview.\n\nTo start off: {question_meta.question}"
        
        session_service.save_session(session)
        return InterviewResponse(
            reply=welcome_reply,
            done=False,
            stage=session.stage.value,
            questionNumber=1,
            maxQuestions=15,
            topicsCovered=session.topicsCovered,
            daysCovered=session.daysCovered,
            difficulty=session.difficulty,
            currentTopic=session.currentTopic
        )

    async def process_candidate_turn(self, session_id: str, candidate_message: str) -> InterviewResponse:
        session = session_service.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found.")

        if session.completed:
            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=session.feedback,
                stage=StageEnum.COMPLETED.value,
                questionNumber=session.questionCount,
                maxQuestions=15,
                topicsCovered=session.topicsCovered,
                daysCovered=session.daysCovered,
                difficulty=session.difficulty,
                currentTopic=session.currentTopic
            )

        logger.info(f"Session {session_id} - Turn {session.questionCount + 1} - Msg: {candidate_message[:50]}...")

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

        # Update cumulative strengths & weaknesses
        for s in eval_result.strengths:
            if s not in session.candidateStrengths:
                session.candidateStrengths.append(s)
        for w in eval_result.weaknesses:
            if w not in session.candidateWeaknesses:
                session.candidateWeaknesses.append(w)

        # 4. Adapt difficulty based on score and evaluator action
        if eval_result.recommendedAction in ["INCREASE_DIFFICULTY", "MOVE_TO_SYSTEM_DESIGN"] or eval_result.score >= 8.5:
            if session.difficulty == "Beginner":
                session.difficulty = "Intermediate"
            elif session.difficulty == "Intermediate":
                session.difficulty = "Advanced"
            elif session.difficulty == "Advanced":
                session.difficulty = "System Design"
        elif eval_result.recommendedAction == "DECREASE_DIFFICULTY" or eval_result.score <= 4.0:
            if session.difficulty == "System Design":
                session.difficulty = "Advanced"
            elif session.difficulty == "Advanced":
                session.difficulty = "Intermediate"
            elif session.difficulty == "Intermediate":
                session.difficulty = "Beginner"

        # 5. Check stage progression and evidence-based termination criteria
        q_count = session.questionCount
        unique_days_covered = len(set(session.daysCovered))

        should_finish = False
        if q_count >= 15:
            should_finish = True
        elif q_count >= 8:
            should_finish = True



        if should_finish:
            session.stage = StageEnum.COMPLETED
            session.completed = True
            
            # Generate evidence-based final feedback
            feedback = await feedback_generator_agent.generate_feedback(session)
            session.feedback = feedback
            session_service.save_session(session)

            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=feedback,
                stage=StageEnum.COMPLETED.value,
                questionNumber=q_count,
                maxQuestions=15,
                topicsCovered=session.topicsCovered,
                daysCovered=session.daysCovered,
                difficulty=session.difficulty,
                currentTopic=session.currentTopic
            )

        # Update Stage State Machine adaptively
        if q_count < 2:
            session.stage = StageEnum.BASELINE
        elif q_count < 4:
            session.stage = StageEnum.DEEP_DIVE
        elif q_count < 6:
            session.stage = StageEnum.CROSS_TOPIC
        elif q_count < 8:
            # Strong candidates jump to System Design faster
            session.stage = StageEnum.SYSTEM_DESIGN if eval_result.score >= 7.5 else StageEnum.DEEP_DIVE
        else:
            session.stage = StageEnum.PRODUCTION

        # 6. Plan Next Question / Follow-up
        next_q_meta = await question_planner_agent.plan_question(
            session=session,
            last_answer=candidate_message,
            last_eval=eval_result
        )

        if next_q_meta.day == session.currentDay:
            session.followUpCount += 1
        else:
            session.followUpCount = 0

        session.questions.append(next_q_meta)
        session.currentQuestion = next_q_meta.model_dump()
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
        return InterviewResponse(
            reply=interviewer_reply,
            done=False,
            stage=session.stage.value,
            questionNumber=session.questionCount + 1,
            maxQuestions=15,
            topicsCovered=session.topicsCovered,
            daysCovered=session.daysCovered,
            difficulty=session.difficulty,
            currentTopic=session.currentTopic
        )

interview_service = InterviewService()
