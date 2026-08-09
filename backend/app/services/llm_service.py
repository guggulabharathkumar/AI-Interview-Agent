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


class AdaptiveMockProvider(BaseLLMProvider):
    """Adaptive, Curriculum-Aware Mock LLM Provider for offline & hackathon demo mode."""
    
    def __init__(self):
        # Comprehensive Curriculum Question Bank mapped by Day Number
        self.question_bank = {
            1: {
                "question": "How do virtual environments (.venv) ensure isolation when configuring Python AI packages inside VS Code?",
                "signals": ["dependency isolation", "site-packages", "interpreter path"]
            },
            3: {
                "question": "When connecting your React frontend to a FastAPI backend endpoint, how do you handle CORS and asynchronous state updates?",
                "signals": ["CORS middleware", "fetch API", "async/await", "useState"]
            },
            4: {
                "question": "How do you construct SQL queries using SQLAlchemy to join structured healthcare plan data with patient claim records?",
                "signals": ["SQLAlchemy ORM", "FOREIGN KEY", "JOIN queries", "SQLite"]
            },
            6: {
                "question": "What chunking strategy and metadata tags did you attach when exporting knowledge base documents into knowledge_base.jsonl?",
                "signals": ["chunking strategy", "document metadata", "JSONL format", "token size"]
            },
            7: {
                "question": "How do sentence-transformers convert raw text into high-dimensional vector embeddings, and how do you evaluate semantic clustering with PCA?",
                "signals": ["embedding dimensionality", "dense vector", "cosine similarity", "PCA dimensionality reduction"]
            },
            8: {
                "question": "What are the trade-offs between a local ChromaDB instance and a managed cloud Pinecone vector index for RAG retrieval?",
                "signals": ["ChromaDB local persistence", "Pinecone cloud scaling", "HNSW indexing", "latency vs convenience"]
            },
            10: {
                "question": "In the retrieval engine, how does k-NN similarity search match user query embeddings against indexed document chunks?",
                "signals": ["top-k retrieval", "similarity score threshold", "dense search", "vector index"]
            },
            11: {
                "question": "Walk me through an end-to-end RAG pipeline: from receiving a query to context insertion and final LLM generation.",
                "signals": ["query embedding", "vector database lookup", "context window injection", "grounded prompt"]
            },
            12: {
                "question": "How do system prompts, few-shot examples, and chain-of-thought instructions influence LLM prompt grounding and prevent hallucinations?",
                "signals": ["few-shot prompting", "chain-of-thought", "system role instruction", "hallucination mitigation"]
            },
            13: {
                "question": "Why is Pydantic structured output with function calling superior to parsing free-form LLM text responses in production backend APIs?",
                "signals": ["JSON schema validation", "Pydantic parsing", "tool function call", "deterministic output"]
            },
            16: {
                "question": "How do you architect a FastAPI endpoint to stream tokens using Server-Sent Events (SSE) back to a client interface?",
                "signals": ["StreamingResponse", "async generator", "EventSource client", "token streaming"]
            },
            20: {
                "question": "How do you manage conversation memory when context length approaches the model's context window limit?",
                "signals": ["sliding window memory", "conversation summary buffer", "token counting", "context trimming"]
            },
            21: {
                "question": "What is the key difference between a simple chain and a LangChain Agent equipped with tools and a dynamic execution loop?",
                "signals": ["ReAct framework", "tool execution", "agentic loop", "action plan"]
            },
            22: {
                "question": "In a multi-agent orchestration architecture, how do specialized sub-agents coordinate and hand off execution states?",
                "signals": ["supervisor router", "agent handoff", "shared state object", "task decomposition"]
            },
            23: {
                "question": "How does the Model Context Protocol (MCP) standardize tool discovery and resource invocation across agent frameworks?",
                "signals": ["MCP server spec", "JSON-RPC protocol", "tool registration", "standardized context"]
            },
            25: {
                "question": "How do you measure RAG quality using quantitative evaluation frameworks like Ragas or G-Eval (Faithfulness, Answer Relevance, Context Recall)?",
                "signals": ["Ragas metrics", "faithfulness", "context precision", "evaluation dataset"]
            },
            28: {
                "question": "How do you optimize a Docker container for an AI service to minimize build time and image size?",
                "signals": ["multi-stage build", "python-slim base image", "pip cache", "layer optimization"]
            },
            29: {
                "question": "What key telemetry metrics (TTFT latency, token throughput, failure rates, cost) should you monitor in a production LLM deployment?",
                "signals": ["TTFT latency", "tokens/sec throughput", "tracing span", "cost monitoring"]
            },
            31: {
                "question": "In your final capstone system, how did you handle edge cases where retrieval returned semantically similar but factually incorrect documents?",
                "signals": ["hybrid retrieval", "reranking cross-encoder", "fallback prompt", "guardrail validation"]
            }
        }

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        sys_lower = system_prompt.lower()
        user_lower = user_prompt.lower()

        # 1. Question Planner Agent JSON
        if "question planner" in sys_lower or "plan the next question" in sys_lower:
            day_num = 7
            import re
            match = re.search(r"selected curriculum day:\s*day\s*(\d+)", user_lower)
            if match:
                day_num = int(match.group(1))
            else:
                for d in [10, 11, 12, 13, 16, 20, 21, 22, 23, 25, 28, 29, 31, 8, 7, 6, 4, 3, 1]:
                    if f"day {d}" in user_lower:
                        day_num = d
                        break

            q_info = self.question_bank.get(day_num, self.question_bank.get(7, {
                "question": f"Can you explain your technical implementation for Day {day_num}?",
                "signals": ["technical implementation", "architecture"]
            }))
            return {
                "question": q_info["question"],
                "day": day_num,
                "topic": f"Cohort Topic Day {day_num}",
                "difficulty": "Intermediate",
                "type": "conceptual",
                "purpose": f"Assess candidate technical depth on Day {day_num}",
                "expectedSignals": q_info["signals"]
            }


        # 2. Answer Evaluator Agent JSON
        if "evaluator" in sys_lower or "evaluate" in sys_lower:
            length = len(user_prompt)
            keywords = ["vector", "embedding", "rag", "api", "docker", "agent", "prompt", "similarity", "retrieval", "db", "latency", "chunk", "context", "pydantic", "mcp", "streaming"]
            matched = [kw for kw in keywords if kw in user_lower]
            kw_count = len(matched)

            if length > 90 and kw_count >= 2:
                # Strong detailed answer
                return {
                    "score": 8.8,
                    "correctness": 9.0,
                    "depth": 8.5,
                    "reasoning": 8.5,
                    "practicality": 9.0,
                    "confidence": 8.8,
                    "missingConcepts": ["edge-case failure recovery under extreme load"],
                    "misconceptions": [],
                    "strengths": ["Articulated core mechanism cleanly", f"Used precise technical vocabulary ({', '.join(matched[:3])})"],
                    "weaknesses": ["Could expand slightly on production scaling trade-offs"],
                    "recommendedAction": "FOLLOW_UP_DEEPER",
                    "followUpType": "FOLLOW_UP_TRADEOFF"
                }
            elif length > 40:
                # Partial answer
                return {
                    "score": 6.2,
                    "correctness": 6.5,
                    "depth": 5.8,
                    "reasoning": 6.0,
                    "practicality": 6.0,
                    "confidence": 6.5,
                    "missingConcepts": ["concrete step-by-step implementation details"],
                    "misconceptions": [],
                    "strengths": ["Understands high-level concept"],
                    "weaknesses": ["Answer lacks granular technical implementation mechanics"],
                    "recommendedAction": "FOLLOW_UP_CLARIFY",
                    "followUpType": "FOLLOW_UP_CLARIFY"
                }
            else:
                # Weak answer
                return {
                    "score": 3.8,
                    "correctness": 4.0,
                    "depth": 3.0,
                    "reasoning": 3.5,
                    "practicality": 3.5,
                    "confidence": 4.0,
                    "missingConcepts": ["fundamental mechanism definition"],
                    "misconceptions": ["Vague generalization without technical specificity"],
                    "strengths": ["Attempted candidate response"],
                    "weaknesses": ["Response is vague and incomplete"],
                    "recommendedAction": "DECREASE_DIFFICULTY",
                    "followUpType": "FOLLOW_UP_CLARIFY"
                }

        # 3. Final Feedback Generator JSON
        if "feedback" in sys_lower or "generate feedback" in sys_lower:
            return {
                "summary": "Demonstrated strong understanding of core RAG architecture, vector embeddings, and backend API integration with good engineering clarity.",
                "strengths": [
                    "Explained the dense vector transformation mechanism and similarity distance search clearly.",
                    "Articulated backend API design, context management, and Pydantic structured output handling.",
                    "Demonstrated good awareness of prompt engineering and agentic workflow orchestration."
                ],
                "gaps": [
                    "Needs deeper focus on retrieval failure mode handling and hybrid sparse-dense search.",
                    "Could expand on containerized deployment optimization and production observability metrics."
                ],
                "next": [
                    "Practice building hybrid retrieval (BM25 + Dense) with cross-encoder reranking.",
                    "Implement end-to-end tracing and telemetry monitoring for deployed AI microservices.",
                    "Design and benchmark multi-agent systems using Model Context Protocol (MCP)."
                ]
            }

        return {"status": "ok"}

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        user_lower = user_prompt.lower()

        # Follow-up generation based on evaluator action and user prompt content
        if "evaluator action recommendation: follow_up_deeper" in user_lower or "follow_up_tradeoff" in user_lower:
            return "Good response. Now, suppose your system experiences high traffic and strict latency SLA requirements. What specific architectural trade-offs would you make to maintain retrieval accuracy while optimizing latency?"

        if "evaluator action recommendation: follow_up_clarify" in user_lower:
            return "Thank you for that overview. Could you clarify the exact step between generating the document embedding and querying the vector index?"

        if "evaluator action recommendation: decrease_difficulty" in user_lower:
            return "Let's step back to the core concept. In simple terms, how would you define the main role of this component in the pipeline?"

        # Default fallback text
        return "Thank you for explaining that. Let's examine how this concept connects with system architecture in production."


def get_llm_provider() -> BaseLLMProvider:
    """Factory function returning active LLM Provider."""
    if settings.is_demo_mode:
        logger.info("Using AdaptiveMockProvider (Demo/Local Mode)")
        return AdaptiveMockProvider()
    else:
        logger.info(f"Using OpenAIProvider with model {settings.OPENAI_MODEL}")
        return OpenAIProvider(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL)
