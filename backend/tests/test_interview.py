import asyncio
import pytest
import httpx
from app.main import app
from app.services.candidate_service import candidate_service

def test_full_interview_flow():
    async def run():
        candidates = candidate_service.get_all_candidates()
        assert len(candidates) >= 2
        cand1 = candidates[0].model_dump()

        session_id = "test-flow-101"

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            # 1. Start Interview
            start_payload = {
                "sessionId": session_id,
                "candidate": cand1
            }
            response = await ac.post("/api/interview", json=start_payload)
            assert response.status_code == 200
            res_data = response.json()
            assert res_data["done"] is False
            assert "reply" in res_data
            assert len(res_data["reply"]) > 0

            # 2. Conduct multi-turn conversation (send 9 messages to exceed minimum 8 turns)
            sample_answers = [
                "Embeddings convert text into dense vectors so we can perform semantic vector distance search.",
                "We store vectors in ChromaDB or Pinecone and use cosine similarity to retrieve relevant document chunks.",
                "RAG combines vector retrieval with an LLM prompt context to answer questions grounded in private data.",
                "System prompt engineering ensures the model returns structured JSON and adheres to constraints.",
                "For multi-agent systems, we orchestrate agents using routers and Model Context Protocol for tool invocation.",
                "Docker containerization helps isolate dependencies and scale backend services efficiently.",
                "We monitor latency, token usage, and accuracy metrics using tracing and structured logging tools.",
                "To optimize costs, we cache embedding results and use smaller fine-tuned models where appropriate.",
                "Final summary response demonstrating comprehensive engineering knowledge."
            ]

            final_response = None
            for idx, ans in enumerate(sample_answers):
                turn_payload = {
                    "sessionId": session_id,
                    "message": ans
                }
                res = await ac.post("/api/interview", json=turn_payload)
                assert res.status_code == 200
                final_response = res.json()
                if final_response["done"]:
                    break

            # 3. Assert completion and feedback structure
            assert final_response["done"] is True
            assert "feedback" in final_response
            fb = final_response["feedback"]
            assert "summary" in fb and len(fb["summary"]) > 0
            assert "strengths" in fb and isinstance(fb["strengths"], list) and len(fb["strengths"]) > 0
            assert "gaps" in fb and isinstance(fb["gaps"], list) and len(fb["gaps"]) > 0
            assert "next" in fb and isinstance(fb["next"], list) and len(fb["next"]) > 0

            # 4. Check completed session rejects or returns completed
            extra_turn = await ac.post("/api/interview", json={"sessionId": session_id, "message": "hello"})
            assert extra_turn.status_code == 200
            assert extra_turn.json()["done"] is True

    asyncio.run(run())

def test_candidate_differentiation():
    async def run():
        candidates = candidate_service.get_all_candidates()
        cand1 = candidates[0].model_dump()
        cand3 = candidates[2].model_dump() # Emily Chen (AI Engineer) vs Sarah Johnson (Data Eng)

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            res1 = await ac.post("/api/interview", json={"sessionId": "diff-001", "candidate": cand1})
            res3 = await ac.post("/api/interview", json={"sessionId": "diff-002", "candidate": cand3})

            assert res1.status_code == 200
            assert res3.status_code == 200
            assert res1.json()["reply"] != res3.json()["reply"]

    asyncio.run(run())
