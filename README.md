# AI Interview Agent

### *"Build the interviewer, not the interview."*

AI Interview Agent is an autonomous, curriculum-aware, adaptive technical interviewer system. Rather than asking a fixed list of static questions, it analyzes a candidate's cohort learning history, dynamically constructs persona-aware technical questions, adaptively probes responses with deep multi-turn follow-ups, and delivers structured, actionable final feedback.

---

## 💡 Problem

Traditional technical assessment tools rely on rigid, scripted question banks or multiple-choice quizzes that fail to test how engineers actually think, reason about architectural trade-offs, handle edge cases, or debug complex AI applications. 

## 🚀 Solution

AI Interview Agent acts as an expert technical interviewer:
- **Candidate-Aware Personalization**: Reads candidate signals (passed, failed, skipped missions, attempt counts, commit frequency, experience level).
- **Adaptive State Machine**: Dynamically shifts stages (`INTRO` → `BASELINE` → `DEEP_DIVE` → `CROSS_TOPIC` → `SYSTEM_DESIGN` → `PRODUCTION` → `FINAL_EVALUATION`).
- **Multi-Turn Probing Engine**: Evaluates answers for correctness, depth, and missing concepts to ask targeted follow-ups.
- **Curriculum Grounding**: Integrates a 31-day, 8-module AI curriculum covering embeddings, vector databases, RAG, agents, MCP, evaluation, security, and production deployment.

---

## 🏗 Architecture

```
+-------------------------------------------------------------+
|                      React Frontend                         |
|      (Candidate Selector, Live Chat, Feedback Dashboard)     |
+-------------------------------------------------------------+
                                |
                        POST /api/interview
                                v
+-------------------------------------------------------------+
|                     FastAPI Backend                         |
+-------------------------------------------------------------+
       |                        |                       |
       v                        v                       v
+---------------+    +--------------------+    +--------------------+
| Session       |    | Candidate          |    | Curriculum         |
| Service       |    | Personalization    |    | Service            |
+---------------+    +--------------------+    +--------------------+
       |                        |                       |
       +------------------------+-----------------------+
                                |
                                v
                 +----------------------------+
                 |  Interview Service Engine  |
                 +----------------------------+
                     /          |          \
                    v           v           v
       +------------------+ +-----------+ +------------------+
       | Question Planner | | Evaluator | | Interviewer      |
       | Agent            | | Agent     | | Agent            |
       +------------------+ +-----------+ +------------------+
                    \           |           /
                     v          v          v
          +-------------------------------------------+
          | LLM Provider Abstraction                  |
          | (OpenAI API  <or>  Deterministic Mock)    |
          +-------------------------------------------+
                                |
                                v
                 +----------------------------+
                 | Feedback Generator Agent   |
                 +----------------------------+
```

---

## ✨ Features

- **Multi-Turn Conversation Memory**: Tracks previous questions, candidate answers, evaluated scores, covered curriculum days, and stage context across HTTP requests using `sessionId`.
- **Candidate Personalization Engine**: Differentiates between roles (AI Engineer, Backend, DevOps, Data Engineer, Business Analyst) and tailors question depth accordingly.
- **Curriculum-Aware Planning**: Ensures interviews cover at least 4 distinct curriculum days and 8–15 adaptive turns.
- **Structured Feedback Dashboard**: Outputs standardized evaluation JSON (`summary`, `strengths`, `gaps`, `next`).
- **Zero-Dependency Demo / Mock Mode**: Runs out of the box without requiring external API keys.

---

## 🛠 Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic v2, Pytest, Uvicorn
- **Frontend**: React 18, Vite, Lucide Icons, Modern Vanilla CSS
- **AI/LLM Integration**: OpenAI API (`gpt-4o-mini`) with fallback to `MockProvider`
- **Containerization**: Docker, Docker Compose

---

## ⚙️ Local Setup & Quickstart

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
Backend API server will start at `http://localhost:8000`.

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend web app will open at `http://localhost:5173`.

---

## 🔑 Environment Configuration

Copy `.env.example` to `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
LLM_PROVIDER=openai
DEMO_MODE=true
```

If `OPENAI_API_KEY` is not set or `DEMO_MODE=true`, the system automatically activates `MockProvider`.

---

## 📡 API Contract

### POST `/api/interview`

#### Start Interview Request
```json
POST /api/interview
{
  "sessionId": "demo-session-001",
  "candidate": {
    "member": {
      "id": "CAND-001",
      "name": "Sarah Johnson",
      "jobRole": "Senior Data Engineer",
      "yearsExperience": 9,
      "education": "MS Computer Science",
      "status": "COMPLETED"
    },
    "missions": [ ... ],
    "signals": { "commitDays": 28, "missionsCompleted": 30, "missionsFirstTry": 20 }
  }
}
```

#### Start Response
```json
{
  "reply": "Welcome Sarah Johnson. Let's begin your technical interview.\n\nTo start off: Can you explain how embeddings convert text into dense vectors for similarity search?",
  "done": false
}
```

#### Subsequent Turn Request
```json
POST /api/interview
{
  "sessionId": "demo-session-001",
  "message": "Embeddings convert text into dense vectors so we can search semantically using cosine distance."
}
```

#### Turn Response
```json
{
  "reply": "Good explanation. Now suppose your vector search returns semantically similar results that are irrelevant to the user's question. What would you investigate?",
  "done": false
}
```

#### Final Response (Interview Completion)
```json
{
  "reply": "Interview completed.",
  "done": true,
  "feedback": {
    "summary": "Demonstrated solid technical grasp of RAG architecture, vector search principles, and multi-agent coordination with good practical clarity.",
    "strengths": [
      "Clearly explained the mechanism of dense vector embeddings for semantic retrieval.",
      "Articulated backend API design and context management cleanly."
    ],
    "gaps": [
      "Needs deeper focus on retrieval failure mode handling and vector indexing strategies."
    ],
    "next": [
      "Practice building hybrid sparse-dense retrieval pipelines with reranking."
    ]
  }
}
```

---

## 🧪 Testing

Run backend test suite using Pytest:

```bash
pytest backend/tests -v
```

---

## 🐳 Docker Deployment

To launch the full backend and frontend stack in containers:

```bash
docker compose up --build
```

Access the frontend app at `http://localhost:5173`.

---

## 📐 Design Decisions

1. **State Machine Architecture**: Guarantees logical progression through interview stages (`BASELINE` → `DEEP_DIVE` → `CROSS_TOPIC` → `SYSTEM_DESIGN` → `PRODUCTION`).
2. **Personalization Engine**: Avoids standard scripted questions by indexing candidate cohort data (passed, failed, skipped missions) to ground every question.
3. **Agent Separation**: Decouples Question Planning, Answer Evaluation, Interviewer Persona, and Feedback Generation into distinct agent responsibilities.
4. **Mock Provider**: Enables testing and evaluation out of the box without requiring external API tokens.
