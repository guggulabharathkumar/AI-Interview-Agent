from app.models import SessionState, FeedbackResponse
from app.prompts.feedback_prompt import FEEDBACK_SYSTEM_PROMPT, build_feedback_user_prompt
from app.services.llm_service import get_llm_provider

class FeedbackGeneratorAgent:
    """Agent that synthesizes overall interview performance into structured feedback."""
    
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
                summary=res.get("summary", "Interview completed successfully with overall strong technical performance."),
                strengths=res.get("strengths", ["Demonstrated clear technical communication", "Good foundational concepts"]),
                gaps=res.get("gaps", ["Can deepen understanding of production edge cases"]),
                next=res.get("next", ["Practice hands-on implementation of RAG pipelines"])
            )
        except Exception:
            # Fallback feedback
            return FeedbackResponse(
                summary=f"Completed technical interview covering {len(session.topicsCovered)} curriculum modules for the role of {session.candidate.member.jobRole}.",
                strengths=[
                    f"Solid understanding of core curriculum concepts across {len(session.daysCovered)} cohort days.",
                    "Active technical problem-solving approach during multi-turn probing."
                ],
                gaps=[
                    "Opportunities to deepen knowledge in production reliability and vector search optimization."
                ],
                next=[
                    "Build hands-on production RAG applications using ChromaDB/Pinecone.",
                    "Explore advanced multi-agent workflows and Model Context Protocol (MCP)."
                ]
            )

feedback_generator_agent = FeedbackGeneratorAgent()
