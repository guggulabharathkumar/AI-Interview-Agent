from app.models import SessionState, QuestionMetadata, EvaluationResult
from app.prompts.interviewer_prompt import INTERVIEWER_SYSTEM_PROMPT, build_interviewer_user_prompt
from app.services.llm_service import get_llm_provider

class InterviewerAgent:
    """Main Interviewer Agent that communicates with candidate."""
    
    def __init__(self):
        self.llm = get_llm_provider()

    async def generate_response(
        self,
        session: SessionState,
        question_meta: QuestionMetadata,
        candidate_last_answer: str = "",
        last_eval: EvaluationResult = None
    ) -> str:
        user_prompt = build_interviewer_user_prompt(
            candidate_name=session.candidate.member.name,
            job_role=session.candidate.member.jobRole,
            years_exp=session.candidate.member.yearsExperience,
            stage=session.stage.value,
            difficulty=session.difficulty,
            current_topic=question_meta.topic,
            question_purpose=question_meta.purpose,
            planned_question=question_meta.question,
            candidate_last_answer=candidate_last_answer,
            eval_action=last_eval.recommendedAction if last_eval else ""
        )

        reply = await self.llm.generate_text(INTERVIEWER_SYSTEM_PROMPT, user_prompt)
        
        # Clean up any potential AI markdown artifacts or metadata leakage
        cleaned_reply = reply.strip().strip('"')
        if not cleaned_reply:
            cleaned_reply = question_meta.question
            
        return cleaned_reply

interviewer_agent = InterviewerAgent()
