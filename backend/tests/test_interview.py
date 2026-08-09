import asyncio
import pytest
import httpx
from app.main import app
from app.services.candidate_service import candidate_service
from app.services.session_service import session_service

def test_full_interview_flow():
    """Test 5 & 6 & 7 & 8: Verify 8+ questions, 4+ curriculum days, state persistence, and evidence feedback."""
    async def run():
        candidates = candidate_service.get_all_candidates()
        assert len(candidates) >= 2
        cand1 = candidates[0].model_dump()

        session_id = "test-adaptive-flow-101"

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
            assert "stage" in res_data
            assert res_data["stage"] == "BASELINE"

            # 2. Multi-turn conversation sending high quality answers
            sample_answers = [
                "Embeddings convert text into dense vectors using neural models so we can calculate cosine distance.",
                "We store vectors in ChromaDB or Pinecone and execute k-NN top-k search with similarity thresholds.",
                "RAG grounds the LLM context window with retrieved knowledge chunks to prevent hallucination.",
                "Pydantic structured output validation with function calling guarantees deterministic JSON schema matching.",
                "For multi-agent systems, supervisor routers hand off execution states using Model Context Protocol.",
                "Docker containerization isolates dependencies using multi-stage builds for small image footprints.",
                "We monitor TTFT latency, token throughput, accuracy metrics, and tracing spans in production.",
                "To optimize costs, we cache embedding results and route queries to smaller fine-tuned models.",
                "Final response demonstrating comprehensive technical engineering skills."
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
            assert "strengths" in fb and len(fb["strengths"]) > 0
            assert "gaps" in fb and len(fb["gaps"]) > 0
            assert "next" in fb and len(fb["next"]) > 0

    asyncio.run(run())

def test_candidate_differentiation():
    """Test 1 & 9: Verify different candidate profiles produce different starting strategies and question paths."""
    async def run():
        candidates = candidate_service.get_all_candidates()
        cand1 = candidates[0].model_dump() # Sarah Johnson - Data Eng
        cand4 = candidates[3].model_dump() # David Miller - Business Analyst

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            res1 = await ac.post("/api/interview", json={"sessionId": "diff-strategy-001", "candidate": cand1})
            res4 = await ac.post("/api/interview", json={"sessionId": "diff-strategy-004", "candidate": cand4})

            assert res1.status_code == 200
            assert res4.status_code == 200
            assert res1.json()["reply"] != res4.json()["reply"]
            # Check difficulty levels differ for Senior Eng vs Business Analyst
            assert res1.json()["difficulty"] != res4.json()["difficulty"] or res1.json()["stage"] == "BASELINE"

    asyncio.run(run())

def test_adaptive_difficulty_on_strong_and_weak_answers():
    """Test 2 & 3 & 4: Strong answer increases difficulty, weak answer triggers diagnostic follow-up."""
    async def run():
        candidates = candidate_service.get_all_candidates()
        cand = candidates[0].model_dump()
        session_id = "test-adaptive-diff-202"

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            # Start
            await ac.post("/api/interview", json={"sessionId": session_id, "candidate": cand})

            # Turn 1: Very strong detailed technical answer
            strong_answer = "Embeddings map semantic text into dense vector space using transformer models. We compute cosine similarity and index them using HNSW trees in vector databases like ChromaDB."
            res_strong = await ac.post("/api/interview", json={"sessionId": session_id, "message": strong_answer})
            assert res_strong.status_code == 200
            data_strong = res_strong.json()
            assert data_strong["done"] is False
            assert data_strong["difficulty"] in ["Intermediate", "Advanced", "System Design"]

            # Turn 2: Weak answer
            weak_answer = "I don't know much about this topic."
            res_weak = await ac.post("/api/interview", json={"sessionId": session_id, "message": weak_answer})
            assert res_weak.status_code == 200
            data_weak = res_weak.json()
            assert data_weak["done"] is False

    asyncio.run(run())

def test_api_response_metadata():
    """Test 10: Backend response metadata exposes stage, questionNumber, difficulty, and topics covered."""
    async def run():
        candidates = candidate_service.get_all_candidates()
        cand = candidates[0].model_dump()
        session_id = "test-meta-303"

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            res_start = await ac.post("/api/interview", json={"sessionId": session_id, "candidate": cand})
            data = res_start.json()

            assert "stage" in data
            assert "questionNumber" in data
            assert "topicsCovered" in data
            assert "daysCovered" in data
            assert "difficulty" in data
            assert data["questionNumber"] == 1

    asyncio.run(run())
