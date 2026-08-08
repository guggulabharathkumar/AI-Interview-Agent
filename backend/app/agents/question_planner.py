import random
from typing import List, Optional
from app.models import SessionState, QuestionMetadata, StageEnum
from app.services.curriculum_service import curriculum_service
from app.services.llm_service import get_llm_provider

QUESTION_PLANNER_SYSTEM_PROMPT = """You are a Technical Question Planner Agent.
Your job is to select the next curriculum topic, question type, and purpose for an ongoing AI engineering interview.

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
    """Agent that plans curriculum topics and question metadata."""
    
    def __init__(self):
        self.llm = get_llm_provider()

    async def plan_question(self, session: SessionState) -> QuestionMetadata:
        profile = session.analyzedProfile
        stage = session.stage
        all_days = curriculum_service.get_all_days()
        
        # Determine candidate completed/weak/skipped day numbers
        passed_days = [m.day for m in session.candidate.missions if m.passed]
        skipped_days = [m.day for m in session.candidate.missions if m.skipped]
        
        # Ensure curriculum coverage across 4+ days
        used_days = set(session.daysCovered)
        available_days = [d for d in all_days if d.day not in used_days]
        if not available_days:
            available_days = all_days

        # Pick target day based on stage and candidate background
        target_day_obj = None
        
        if stage == StageEnum.BASELINE:
            # Baseline question from a passed strength topic or day 7
            candidate_passed_objs = [d for d in all_days if d.day in passed_days]
            target_day_obj = candidate_passed_objs[0] if candidate_passed_objs else all_days[2] # Day 7 (Embeddings)
            
        elif stage == StageEnum.DEEP_DIVE:
            # Deep dive on current day or next un-covered day
            if session.currentDay:
                target_day_obj = curriculum_service.get_day(session.currentDay)
            if not target_day_obj:
                target_day_obj = available_days[0]
                
        elif stage == StageEnum.CROSS_TOPIC:
            # Connect two topics e.g. Day 7/10 + Day 11/12 or Day 21/22 + Day 23
            target_day_obj = available_days[0] if available_days else all_days[5]
            
        elif stage == StageEnum.SYSTEM_DESIGN:
            # Architecture / RAG / Agents (Day 16, 21, 22)
            sys_days = [d for d in available_days if d.day in [16, 21, 22, 23]]
            target_day_obj = sys_days[0] if sys_days else available_days[0]
            
        elif stage == StageEnum.PRODUCTION:
            # Production, Deployment, Security, Observability (Day 25, 27, 28, 29, 30)
            prod_days = [d for d in all_days if d.day in [25, 27, 28, 29, 30]]
            target_day_obj = prod_days[0] if prod_days else available_days[0]
            
        else:
            target_day_obj = available_days[0] if available_days else all_days[0]

        target_day = target_day_obj.day
        target_topic = target_day_obj.title
        
        # Difficulty selection
        difficulty = session.difficulty

        # Prompt LLM to format QuestionMetadata
        user_prompt = f"""Candidate Role: {session.candidate.member.jobRole}
Candidate Experience: {session.candidate.member.yearsExperience} yrs ({profile.experienceLevel})
Stage: {stage.value}
Difficulty: {difficulty}
Selected Curriculum Day: Day {target_day} - {target_topic}
Tools in topic: {target_day_obj.tools}
Objectives: {target_day_obj.objectives}
Already Covered Days: {list(used_days)}

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
        except Exception as e:
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
