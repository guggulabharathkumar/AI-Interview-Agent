from app.models import SessionState, FeedbackResponse
from app.prompts.feedback_prompt import FEEDBACK_SYSTEM_PROMPT, build_feedback_user_prompt
from app.services.llm_service import get_llm_provider

class FeedbackGeneratorAgent:
    """Agent that synthesizes overall candidate interview performance into evidence-based structured feedback."""
    
    def __init__(self):
        self.llm = get_llm_provider()

    async def generate_feedback(self, session: SessionState) -> FeedbackResponse:
        user_prompt = build_feedback_user_prompt(
            candidate_name=session.candidate.member.name,
            candidate_role=session.candidate.member.jobRole,
            questions=session.questions,
            answers=session.answers,
            evaluations=session.evaluations,
            topics_covered=session.topicsCovered
        )

        try:
            res = await self.llm.generate_json(FEEDBACK_SYSTEM_PROMPT, user_prompt)
            return FeedbackResponse(
                summary=res.get("summary", f"Demonstrated solid technical understanding across {len(session.topicsCovered)} curriculum modules for the role of {session.candidate.member.jobRole}."),
                strengths=res.get("strengths", [
                    f"Articulated core principles of {session.topicsCovered[0] if session.topicsCovered else 'AI systems'} effectively.",
                    "Demonstrated good practical problem-solving during multi-turn technical probing."
                ]),
                gaps=res.get("gaps", [
                    "Opportunities to deepen understanding of production failure mode handling and observability."
                ]),
                next=res.get("next", [
                    "Practice building hybrid retrieval pipelines with cross-encoder reranking.",
                    "Design and benchmark production container deployment and monitoring."
                ])
            )
        except Exception:
            # Evidence-based fallback feedback generated from actual session turns
            strengths_list = []
            gaps_list = []
            
            for q, a, ev in zip(session.questions, session.answers, session.evaluations):
                if ev.score >= 7.5:
                    strengths_list.append(f"Clearly explained {q.topic} principles with solid technical terms.")
                else:
                    gaps_list.append(f"Answer on {q.topic} lacked granular technical implementation depth.")

            if not strengths_list:
                strengths_list = [f"Attempted questions across {len(session.daysCovered)} cohort curriculum days."]
            if not gaps_list:
                gaps_list = ["Can deepen focus on production scaling edge cases."]

            return FeedbackResponse(
                summary=f"Completed comprehensive technical interview for {session.candidate.member.name} ({session.candidate.member.jobRole}), assessing {len(session.questions)} technical questions across {len(session.daysCovered)} curriculum days.",
                strengths=strengths_list[:3],
                gaps=gaps_list[:2],
                next=[
                    f"Practice hands-on implementation of {session.topicsCovered[0] if session.topicsCovered else 'RAG architectures'}.",
                    "Study production containerization, security policies, and telemetry observability.",
                    "Architect multi-agent orchestration systems using Model Context Protocol (MCP)."
                ]
            )

feedback_generator_agent = FeedbackGeneratorAgent()
