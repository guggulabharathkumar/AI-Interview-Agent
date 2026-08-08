import asyncio
import pytest
import httpx
from app.main import app

def test_health_endpoint():
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "demo_mode" in data
            assert "provider" in data

    asyncio.run(run())
