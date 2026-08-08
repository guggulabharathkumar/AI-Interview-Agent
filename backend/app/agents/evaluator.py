from app.models import EvaluationResult, QuestionMetadata
from app.prompts.evaluator_prompt import EVALUATOR_SYSTEM_PROMPT, build_evaluator_user_prompt
from app.services.llm_service import get_llm_provider

class EvaluatorAgent:
    """Agent that evaluates candidate answers for technical depth and correctness."""
    
    def __init__(self):
        self.llm = get_llm_provider()

    async def evaluate_answer(
        self,
        question_meta: QuestionMetadata,
        candidate_answer: str,
        candidate_role: str
    ) -> EvaluationResult:
        user_prompt = build_evaluator_user_prompt(
            question=question_meta.question,
            expected_signals=question_meta.expectedSignals,
            candidate_answer=candidate_answer,
            candidate_role=candidate_role
        )

        try:
            res = await self.llm.generate_json(EVALUATOR_SYSTEM_PROMPT, user_prompt)
            return EvaluationResult(
                score=float(res.get("score", 7.0)),
                correct=bool(res.get("correct", True)),
                depth=float(res.get("depth", 7.0)),
                confidence=float(res.get("confidence", 7.0)),
                missingConcepts=res.get("missingConcepts", []),
                strengths=res.get("strengths", []),
                weaknesses=res.get("weaknesses", []),
                recommendedAction=res.get("recommendedAction", "FOLLOW_UP_DEEPER")
            )
        except Exception:
            # Deterministic fallback evaluation based on candidate answer heuristics
            length = len(candidate_answer.strip())
            is_detailed = length > 60
            return EvaluationResult(
                score=8.0 if is_detailed else 5.0,
                correct=True if is_detailed else False,
                depth=7.5 if is_detailed else 4.5,
                confidence=8.0 if is_detailed else 5.0,
                missingConcepts=[] if is_detailed else ["detailed implementation reasoning"],
                strengths=["Gave a direct response"] if is_detailed else [],
                weaknesses=[] if is_detailed else ["Brief response lacking technical detail"],
                recommendedAction="FOLLOW_UP_DEEPER" if is_detailed else "FOLLOW_UP_CLARIFY"
            )

evaluator_agent = EvaluatorAgent()
