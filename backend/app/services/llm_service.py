import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import openai
from app.config import settings

logger = logging.getLogger("ai_interview_agent.llm")

class BaseLLMProvider(ABC):
    """Abstract Base Class for LLM Providers."""
    
    @abstractmethod
    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generates structured JSON response from LLM."""
        pass

    @abstractmethod
    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """Generates plain text string response from LLM."""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API implementation using AsyncOpenAI."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt + "\nReturn strictly valid JSON."},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.4
            )
            raw = response.choices[0].message.content or "{}"
            return json.loads(raw)
        except Exception as e:
            logger.error(f"OpenAI JSON Generation error: {e}")
            raise RuntimeError(f"LLM API Error: {str(e)}")

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.6
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI Text Generation error: {e}")
            raise RuntimeError(f"LLM API Error: {str(e)}")


class MockProvider(BaseLLMProvider):
    """Deterministic Mock LLM Provider for local testing & demo mode."""
    
    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        user_prompt_lower = user_prompt.lower()
        
        # 1. Question Planner check
        if "question planner" in system_prompt.lower() or "plan the next question" in system_prompt.lower():
            day = 7
            if "day 10" in user_prompt or "retrieval" in user_prompt_lower:
                day = 10
            elif "day 12" in user_prompt or "prompt" in user_prompt_lower:
                day = 12
            elif "day 16" in user_prompt or "api" in user_prompt_lower:
                day = 16
            elif "day 22" in user_prompt or "agent" in user_prompt_lower:
                day = 22
            elif "day 28" in user_prompt or "docker" in user_prompt_lower:
                day = 28
            
            return {
                "question": "Can you explain how embeddings convert textual semantics into dense vectors for similarity search?",
                "day": day,
                "topic": "Embeddings & Retrieval Engine",
                "difficulty": "Intermediate",
                "type": "conceptual",
                "purpose": "Assess candidate understanding of vector space semantics",
                "expectedSignals": ["vector distance", "cosine similarity", "semantic search"]
            }

        # 2. Evaluator check
        if "evaluator" in system_prompt.lower() or "evaluate" in system_prompt.lower():
            # Analyze answer quality based on user_prompt
            length = len(user_prompt)
            has_keywords = any(kw in user_prompt_lower for kw in ["vector", "embedding", "rag", "api", "docker", "agent", "prompt", "similarity", "retrieval", "db", "latency", "chunk", "context"])
            
            if length > 80 and has_keywords:
                return {
                    "score": 8.5,
                    "correct": True,
                    "depth": 8.0,
                    "confidence": 8.5,
                    "missingConcepts": ["production scaling trade-offs"],
                    "strengths": ["Solid explanation of high-level architecture", "Clear technical terminology"],
                    "weaknesses": ["Could expand on failure modes and edge cases"],
                    "recommendedAction": "FOLLOW_UP_DEEPER"
                }
            elif length > 30:
                return {
                    "score": 6.0,
                    "correct": True,
                    "depth": 5.5,
                    "confidence": 6.0,
                    "missingConcepts": ["practical implementation details", "edge-case handling"],
                    "strengths": ["Understands basic definitions"],
                    "weaknesses": ["Lacks depth on technical implementation"],
                    "recommendedAction": "FOLLOW_UP_CLARIFY"
                }
            else:
                return {
                    "score": 3.5,
                    "correct": False,
                    "depth": 3.0,
                    "confidence": 4.0,
                    "missingConcepts": ["core definitions", "fundamental mechanism"],
                    "strengths": ["Attempted response"],
                    "weaknesses": ["Vague and incomplete explanation"],
                    "recommendedAction": "DECREASE_DIFFICULTY"
                }

        # 3. Final Feedback check
        if "feedback" in system_prompt.lower() or "generate feedback" in system_prompt.lower():
            return {
                "summary": "Demonstrated solid technical grasp of RAG architecture, vector search principles, and multi-agent coordination with good practical clarity.",
                "strengths": [
                    "Clearly explained the mechanism of dense vector embeddings for semantic retrieval.",
                    "Articulated backend API design and context management cleanly.",
                    "Demonstrated good awareness of LLM prompt engineering techniques."
                ],
                "gaps": [
                    "Needs deeper focus on retrieval failure mode handling and vector indexing strategies.",
                    "Could expand on production containerization, security policies, and observability metrics."
                ],
                "next": [
                    "Practice building hybrid sparse-dense retrieval pipelines with reranking.",
                    "Study production container deployment using Docker and Kubernetes observability patterns.",
                    "Architect an end-to-end multi-agent workflow with Model Context Protocol (MCP) integrations."
                ]
            }

        # Default fallback JSON
        return {"status": "ok", "message": "Mock JSON response"}

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        if "welcome" in user_prompt.lower():
            return "Welcome. Let's begin your technical interview."
        return "Thank you for that response. Let's explore the underlying trade-offs in this approach."


def get_llm_provider() -> BaseLLMProvider:
    """Factory to return appropriate LLM Provider based on config."""
    if settings.is_demo_mode:
        logger.info("Using MockProvider (Demo/Local Mode)")
        return MockProvider()
    else:
        logger.info(f"Using OpenAIProvider with model {settings.OPENAI_MODEL}")
        return OpenAIProvider(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL)
