import os
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from app.config import settings
from app.routes.interview import router as interview_router

# Configure Application Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai_interview_agent")

app = FastAPI(
    title="AI Interview Agent API",
    description="Adaptive, curriculum-aware technical interviewer agent",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Interview Agent",
        "demo_mode": settings.is_demo_mode,
        "provider": "MockProvider" if settings.is_demo_mode else settings.LLM_PROVIDER
    }

# Mount Frontend Build Dist for seamless access at http://localhost:8000/
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    logger.info(f"Mounting static frontend build from {frontend_dist}")
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/")
    async def root_redirect():
        return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
