from typing import List, Optional
from app.models import SessionState, QuestionMetadata, StageEnum, EvaluationResult
from app.services.curriculum_service import curriculum_service
from app.services.llm_service import get_llm_provider

QUESTION_PLANNER_SYSTEM_PROMPT = """You are a Technical Question Planner Agent.
Your job is to select the next curriculum topic, question type, and purpose for an ongoing AI engineering interview based on candidate performance and previous answer.

Output JSON Structure Required:
{
  "question": "A proposed draft base question string",
  "day": 10,
  "topic": "Retrieval & Matching Engine",
  "difficulty": "Intermediate",
  "type": "conceptual|practical|debugging|architecture|tradeoff|scenario",
  "purpose": "Core purpose statement",
  "expectedSignals": ["signal1", "signal2"]
}
"""

class QuestionPlannerAgent:
    """Agent that plans curriculum topics and question metadata using smart topic scoring."""
    
    def __init__(self):
        self.llm = get_llm_provider()

    async def plan_question(
        self,
        session: SessionState,
        last_answer: str = "",
        last_eval: Optional[EvaluationResult] = None
    ) -> QuestionMetadata:
        profile = session.analyzedProfile
        stage = session.stage
        
        # Determine if we should stay on current topic for follow-up or pick a new smart topic
        recommended_action = last_eval.recommendedAction if last_eval else "MOVE_TO_NEXT_TOPIC"
        
        # Should we do a direct follow-up on the current topic?
        if last_eval and session.followUpCount < 2 and recommended_action in [
            "FOLLOW_UP_DEEPER", "FOLLOW_UP_CLARIFY", "FOLLOW_UP_SCENARIO", "FOLLOW_UP_DEBUGGING", "FOLLOW_UP_TRADEOFF"
        ] and session.currentDay:
            target_day_obj = curriculum_service.get_day(session.currentDay)
            if not target_day_obj:
                target_day_obj = curriculum_service.select_smart_topic(
                    profile=profile,
                    stage=stage,
                    days_covered=session.daysCovered,
                    last_answer=last_answer,
                    last_eval_score=last_eval.score if last_eval else 7.0
                )
        else:
            # Select new topic using Smart Topic Selection Scoring algorithm
            target_day_obj = curriculum_service.select_smart_topic(
                profile=profile,
                stage=stage,
                days_covered=session.daysCovered,
                last_answer=last_answer,
                last_eval_score=last_eval.score if last_eval else 7.0
            )

        target_day = target_day_obj.day
        target_topic = target_day_obj.title
        difficulty = session.difficulty

        # Prompt LLM to structure QuestionMetadata
        user_prompt = f"""Candidate Role: {session.candidate.member.jobRole} ({profile.roleFocus})
Candidate Experience: {session.candidate.member.yearsExperience} yrs ({profile.experienceLevel})
Stage: {stage.value}
Difficulty: {difficulty}
Selected Curriculum Day: Day {target_day} - {target_topic}
Tools in topic: {target_day_obj.tools}
Objectives: {target_day_obj.objectives}
Already Covered Days: {session.daysCovered}
Last Evaluator Action: {recommended_action}
Last Candidate Answer: "{last_answer}"

Plan the next question metadata now.
"""
        try:
            res_dict = await self.llm.generate_json(QUESTION_PLANNER_SYSTEM_PROMPT, user_prompt)
            return QuestionMetadata(
                question=res_dict.get("question", f"Can you explain your approach to {target_topic}?"),
                day=target_day,
                topic=target_topic,
                difficulty=difficulty,
                type=res_dict.get("type", "conceptual"),
                purpose=res_dict.get("purpose", f"Assess knowledge of {target_topic}"),
                expectedSignals=res_dict.get("expectedSignals", target_day_obj.tools)
            )
        except Exception:
            # Fallback metadata
            return QuestionMetadata(
                question=f"In your work with {target_topic}, how do you apply {target_day_obj.tools[0] if target_day_obj.tools else 'key principles'}?",
                day=target_day,
                topic=target_topic,
                difficulty=difficulty,
                type="conceptual",
                purpose=f"Assess baseline understanding of Day {target_day}",
                expectedSignals=target_day_obj.tools
            )

question_planner_agent = QuestionPlannerAgent()
