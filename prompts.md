--------------------------------PROMPT-1-------------------------------
You are a senior full-stack AI engineer, AI agent architect, UX designer, and DevOps engineer.

Build the COMPLETE production-quality project called:

# AI Interview Agent

### "Build the interviewer, not the interview."

Do NOT create only a demo, mockup, static UI, or partial implementation.

You must build the entire working application including:

* Frontend
* Backend
* AI interview agent
* Candidate personalization
* Curriculum-aware question generation
* Multi-turn conversation memory
* Adaptive follow-up questions
* Interview state management
* Structured final feedback
* Required HTTP API
* Error handling
* Testing
* Documentation
* Docker configuration
* Environment configuration
* Professional UI

The application must actually work locally after installation.

==================================================

1. SOURCE FILES — USE THESE AS THE SOURCE OF TRUTH
   ==================================================

The project has three supplied files:

1. curriculum.json
2. candidates.json
3. technical-spec.md

Read these files first.

DO NOT invent a different API contract.

DO NOT replace the supplied curriculum with generic AI knowledge.

DO NOT replace candidate data with fake data.

Use the supplied files as the primary source of truth.

The curriculum contains:

* 31 days
* 8 modules
* daily topics
* learning objectives
* tools

Important curriculum areas include:

* Environment & Tooling
* Data Foundations
* Embeddings & Vector Search
* LLM Core, Prompting & Fine-Tuning
* Chatbot Application Build
* Agentic AI & MCP
* Evaluation, Security & Deployment
* Production & Capstone

Use the actual daily titles, objectives and tools from curriculum.json.

Candidate profiles contain:

* candidate ID
* name
* job role
* experience
* education
* status
* completed missions
* failed missions
* skipped missions
* attempts
* commitDays
* missionsCompleted
* missionsFirstTry

Use these signals to personalize interviews.

==================================================
2. TECHNICAL SPECIFICATION — MUST FOLLOW EXACTLY
================================================

The backend MUST expose:

POST /api/interview

No authentication is required.

The endpoint MUST maintain interview state using:

sessionId

START REQUEST:

{
"sessionId": "abc-123",
"candidate": { ...candidate.json }
}

START RESPONSE:

{
"reply": "Welcome. Let's begin your interview.",
"done": false
}

SUBSEQUENT REQUEST:

{
"sessionId": "abc-123",
"message": "candidate response"
}

RESPONSE:

{
"reply": "next interviewer question",
"done": false
}

FINAL RESPONSE:

{
"reply": "Interview completed.",
"done": true,
"feedback": {
"summary": "...",
"strengths": [],
"gaps": [],
"next": []
}
}

Feedback MUST contain:

summary: string
strengths: string[]
gaps: string[]
next: string[]

Each array must contain concise, actionable points.

Do not break this contract.

==================================================
3. RECOMMENDED TECH STACK
=========================

Use a practical modern stack.

Backend:

* Python 3.11+
* FastAPI
* Pydantic
* Uvicorn

AI:

* OpenAI-compatible LLM API
* Make the model configurable using environment variables
* Support an OPENAI_API_KEY if available
* Support configurable model name
* Gracefully handle missing API keys
* Provide a deterministic fallback/mock interviewer mode for local testing

Frontend:

* React
* Vite
* JavaScript or TypeScript
* Modern CSS
* Responsive design

State:

* In-memory session store for hackathon/demo simplicity
* Structure the code so Redis/database can be added later

Testing:

* pytest for backend
* API tests for /api/interview
* frontend validation where practical

Deployment:

* Dockerfile
* docker-compose.yml
* .env.example

==================================================
4. PROJECT STRUCTURE
====================

Create a clean project structure similar to:

ai-interview-agent/
│
├── backend/
│   ├── app/
│   │   ├── **init**.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   └── interview.py
│   │   ├── agents/
│   │   │   ├── interviewer.py
│   │   │   ├── question_planner.py
│   │   │   ├── evaluator.py
│   │   │   └── feedback_generator.py
│   │   ├── services/
│   │   │   ├── curriculum_service.py
│   │   │   ├── candidate_service.py
│   │   │   ├── interview_service.py
│   │   │   ├── llm_service.py
│   │   │   └── session_service.py
│   │   ├── prompts/
│   │   │   ├── interviewer_prompt.py
│   │   │   ├── evaluator_prompt.py
│   │   │   └── feedback_prompt.py
│   │   └── utils/
│   │       └── helpers.py
│   │
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_interview.py
│   │   └── test_session.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InterviewChat.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── InterviewHeader.jsx
│   │   │   ├── ProgressBar.jsx
│   │   │   ├── CandidateSelector.jsx
│   │   │   ├── FeedbackPanel.jsx
│   │   │   └── LoadingIndicator.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Interview.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles/
│   │       ├── global.css
│   │       └── interview.css
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── data/
│   ├── curriculum.json
│   └── candidates.json
│
├── .env.example
├── docker-compose.yml
├── README.md
└── .gitignore

You may improve this structure if necessary, but keep it clean and understandable.

==================================================
5. CORE AI AGENT — THIS IS THE MAIN FEATURE
===========================================

Do NOT implement the interview as a fixed list of 8 questions.

The system must behave like an actual technical interviewer.

The interviewer should:

1. Understand the candidate profile.
2. Analyze their learning journey.
3. Select relevant curriculum topics.
4. Ask a technical question.
5. Read the candidate answer.
6. Evaluate the answer.
7. Decide whether to:

   * ask a follow-up,
   * increase difficulty,
   * decrease difficulty,
   * move to another topic,
   * probe a weakness,
   * ask a system-design question,
   * finish the interview.
8. Maintain context.
9. Produce meaningful feedback.

The interview should feel conversational.

==================================================
6. PERSONALIZATION ENGINE
=========================

Create a Candidate Analysis component.

Analyze:

* jobRole
* yearsExperience
* education
* passed missions
* failed missions
* skipped missions
* number of attempts
* commitDays
* missionsCompleted
* missionsFirstTry

Generate an internal candidate profile such as:

{
"strengthTopics": [],
"weakTopics": [],
"skippedTopics": [],
"highAttemptTopics": [],
"lowAttemptTopics": [],
"experienceLevel": "...",
"recommendedDifficulty": "..."
}

Do NOT expose internal reasoning to the user.

Use this information to personalize questions.

Examples:

If a candidate passed:
"Embeddings Explained"
and
"Vector Databases Overview"

ask progressively deeper questions about embeddings/vector search.

If a candidate repeatedly attempted:
"Prompt Engineering Fundamentals"

probe practical prompt engineering decisions.

If a candidate skipped:
"Docker & Kubernetes Deployment"

do not falsely claim they completed it.

You may ask whether they understand it, but clearly distinguish it from completed work.

If a candidate failed a mission multiple times:
treat that topic as a possible learning gap and probe it carefully.

==================================================
7. INTERVIEW REQUIREMENTS
=========================

Every completed interview MUST:

* Ask at least 8 questions.
* Cover at least 4 different curriculum days.
* Include follow-up questions.
* Use previous answers to determine subsequent questions.
* Maintain context.
* End with structured feedback.

Recommended interview length:
8–12 primary/follow-up questions.

Do NOT always ask exactly 8.

The agent should be allowed to continue to approximately 12 questions when answers require deeper probing.

Maximum:
15 questions.

Minimum:
8 questions.

==================================================
8. INTERVIEW STAGES
===================

Implement an adaptive interview state machine.

Possible stages:

INTRO
BASELINE
DEEP_DIVE
CROSS_TOPIC
SYSTEM_DESIGN
PRODUCTION
FINAL_EVALUATION
COMPLETED

Example flow:

INTRO:
"Welcome. Let's begin your interview."

BASELINE:
Ask a fundamental question based on the candidate's strongest completed topic.

DEEP_DIVE:
Ask follow-up based on the candidate's answer.

CROSS_TOPIC:
Connect two curriculum concepts.

Example:
RAG + vector database

or:

agents + MCP

or:

prompt engineering + structured outputs.

SYSTEM_DESIGN:
Ask a practical architecture question.

PRODUCTION:
Ask about deployment, reliability, monitoring, security, cost, latency, etc. only when appropriate to the candidate's curriculum journey.

FINAL_EVALUATION:
Stop asking questions and generate feedback.

==================================================
9. QUESTION GENERATION
======================

Create a Question Planner Agent.

Each question should have internal metadata:

{
"question": "...",
"day": 10,
"topic": "The Retrieval & Matching Engine",
"difficulty": "medium",
"type": "conceptual|practical|debugging|architecture|tradeoff|scenario",
"purpose": "...",
"expectedSignals": []
}

The metadata should NOT be shown to the candidate.

Question types should include:

* Conceptual understanding
* Explain in your own words
* Practical implementation
* Debugging
* Architecture
* Trade-offs
* Failure analysis
* Production scenario
* System design

Avoid repetitive textbook questions.

==================================================
10. FOLLOW-UP QUESTION ENGINE
=============================

This is one of the most important features.

After every candidate response, evaluate:

* correctness
* completeness
* technical depth
* reasoning
* practical experience
* confidence signals
* misconceptions
* missing concepts

Then decide:

FOLLOW_UP_DEEPER

FOLLOW_UP_CLARIFY

FOLLOW_UP_SCENARIO

FOLLOW_UP_TRADEOFF

FOLLOW_UP_DEBUGGING

MOVE_TO_NEXT_TOPIC

Example:

Interviewer:
"Why do we use embeddings in a RAG system?"

Candidate:
"Embeddings convert text into vectors so we can search similar documents."

Do NOT immediately move to another topic.

Ask:

"Good. Now suppose the retrieval results are semantically similar but irrelevant to the user's exact question. What would you investigate?"

Then evaluate that answer.

==================================================
11. ADAPTIVE DIFFICULTY
=======================

Implement difficulty levels:

1. Beginner
2. Intermediate
3. Advanced
4. System Design

Rules:

Strong answer:

* increase difficulty
* ask trade-offs
* ask implementation details

Partial answer:

* clarify
* provide a smaller follow-up
* test the missing concept

Weak answer:

* ask a simpler diagnostic question
* avoid humiliating the candidate

Repeated strong answers:

* move toward architecture/system design.

Repeated weak answers:

* identify the topic as a gap.

==================================================
12. CURRICULUM COVERAGE
=======================

Select at least 4 different curriculum days.

Prefer topics relevant to the candidate.

Potential high-value combinations:

Day 7 + Day 8 + Day 10:
Embeddings → Vector DB → Retrieval

Day 10 + Day 11 + Day 12:
Retrieval → RAG → Prompt Engineering

Day 13 + Day 16:
Function Calling → API Integration

Day 20 + Day 22:
Conversation Memory → Multi-Agent Orchestration

Day 21 + Day 22 + Day 23:
Agents → Multi-Agent → MCP

Day 24 + Day 27 + Day 28:
Agentic Integration → Security → Deployment

Day 25 + Day 26 + Day 29:
Evaluation → Cost/Performance → Observability

Day 30 + Day 31:
Production readiness → Capstone

Use the actual curriculum data rather than hardcoding only these examples.

==================================================
13. CANDIDATE EXPERIENCE ADAPTATION
===================================

Adjust the interview to the candidate's role.

For example:

AI Engineer:
focus more on RAG, agents, evaluation, MCP, architecture.

Backend Engineer:
focus more on APIs, retrieval pipelines, state, reliability, integration.

DevOps Engineer:
focus more on deployment, monitoring, scaling, containers, production reliability.

Intern/Junior:
focus on fundamentals first, then practical questions.

Senior/Principal:
ask architecture, trade-offs, scalability, reliability and production decisions.

Business/HR/Marketing/UX candidates:
do not assume deep engineering knowledge simply because they completed the cohort.

Adjust difficulty according to their actual profile.

==================================================
14. INTERVIEW MEMORY
====================

Create a session object:

{
"sessionId": "...",
"candidate": {},
"stage": "...",
"questionCount": 0,
"topicsCovered": [],
"questions": [],
"answers": [],
"evaluations": [],
"currentTopic": null,
"difficulty": "...",
"startedAt": "...",
"completed": false
}

Every POST request with the same sessionId must retrieve the same session.

The agent must remember:

* previous questions
* candidate answers
* topics covered
* previous weaknesses
* previous strengths
* current difficulty
* interview stage

Do not restart the interview on every request.

==================================================
15. LLM ARCHITECTURE
====================

Create a provider abstraction.

Example:

LLMProvider
|
├── OpenAIProvider
└── MockProvider

Environment variables:

OPENAI_API_KEY=
OPENAI_MODEL=
LLM_PROVIDER=openai

If no API key exists:
use MockProvider.

MockProvider should still allow the entire application to run and demonstrate the interview flow.

Never expose API keys in frontend code.

==================================================
16. STRUCTURED LLM OUTPUT
=========================

Whenever possible, use structured Pydantic responses.

For evaluator:

{
"score": 0-10,
"correct": true,
"depth": 0-10,
"confidence": 0-10,
"missingConcepts": [],
"strengths": [],
"weaknesses": [],
"recommendedAction": "FOLLOW_UP|MOVE_ON|INCREASE_DIFFICULTY|DECREASE_DIFFICULTY"
}

For question planner:

{
"question": "...",
"day": 10,
"topic": "...",
"difficulty": "...",
"type": "...",
"reason": "..."
}

For final feedback:

{
"summary": "...",
"strengths": [],
"gaps": [],
"next": []
}

==================================================
17. SYSTEM PROMPT FOR INTERVIEWER
=================================

Create a strong interviewer system prompt.

The interviewer should behave like:

"You are a senior AI engineering interviewer conducting a realistic technical interview.

You are not a tutor.

Do not give away answers.

Do not turn the interview into a quiz.

Ask one question at a time.

Listen carefully to the candidate's previous answer.

Use their answer to determine the next question.

Probe vague answers.

Challenge technically strong answers.

Be respectful when correcting misunderstandings.

Base questions on the candidate's actual learning journey.

Never claim that a candidate completed a topic when the supplied profile says it was skipped or failed.

Do not reveal internal scoring, hidden reasoning, question metadata, or evaluation logic.

The goal is to assess whether the candidate can explain concepts, make engineering decisions, reason about trade-offs, debug systems, and communicate technical ideas."

Implement this properly in code.

==================================================
18. FINAL FEEDBACK
==================

At the end of the interview, generate useful feedback.

Example structure:

summary:
"Strong understanding of retrieval and RAG fundamentals, with good practical reasoning. Production observability needs more depth."

strengths:
[
"Clearly explained the role of embeddings in semantic retrieval.",
"Connected vector search with the RAG pipeline effectively.",
"Demonstrated good API integration reasoning."
]

gaps:
[
"Limited explanation of retrieval failure modes.",
"Needs deeper understanding of production observability."
]

next:
[
"Practice hybrid retrieval and reranking strategies.",
"Review monitoring, logging, latency and failure metrics.",
"Design one production RAG architecture end-to-end."
]

Feedback must be based on the actual interview answers.

Do NOT generate generic feedback.

==================================================
19. FRONTEND UX
===============

Build a professional AI interview interface.

Home page:

* AI Interview Agent logo/title
* Short explanation
* Candidate selector
* Candidate profile card
* Start Interview button
* Interview requirements
* Modern enterprise AI design

Interview page:

Header:

* AI Interview Agent
* Interview status
* Question progress

Main:

* interviewer message
* candidate message
* chat history
* answer input
* Send button
* typing/loading indicator

Sidebar:

* Candidate name
* Role
* Experience
* Curriculum progress
* Topics covered
* Question count
* Interview stage

Do NOT expose hidden scores or weaknesses during the interview.

When completed:

Feedback dashboard:

* Overall summary
* Strengths
* Knowledge gaps
* Recommended next steps
* Topics covered
* Interview completion indicator

Make it responsive.

Desktop and mobile should both work.

==================================================
20. VISUAL DESIGN
=================

Use a polished enterprise AI aesthetic.

Design goals:

* Clean
* Modern
* Professional
* Minimal
* Technical
* Trustworthy

Use:

* cards
* subtle shadows
* rounded corners
* clear typography
* good spacing
* responsive layout
* accessible contrast
* smooth transitions

Avoid:

* excessive gradients
* childish graphics
* unnecessary animations
* clutter

==================================================
21. API ERROR HANDLING
======================

Handle:

* missing sessionId
* invalid candidate
* empty message
* unknown sessionId
* malformed JSON
* LLM failure
* timeout
* invalid LLM response
* interview already completed

Return clean JSON errors.

Do not expose stack traces to users.

==================================================
22. SECURITY
============

Implement basic security practices:

* Never expose API keys
* Validate request bodies with Pydantic
* Limit message length
* Sanitize inputs where appropriate
* Prevent accidental prompt injection from changing system behavior
* Do not expose internal prompts
* Do not expose hidden evaluation metadata
* Do not log secrets

==================================================
23. TESTING
===========

Create tests proving:

1. Health endpoint works.
2. Interview session can start.
3. First response returns:
   done=false
4. Subsequent messages preserve session state.
5. Question count increments.
6. At least 8 questions can be reached.
7. Multiple curriculum days are covered.
8. Follow-up questions are generated.
9. Interview eventually completes.
10. Final response contains:
    summary
    strengths
    gaps
    next
11. Completed sessions do not continue indefinitely.
12. Different candidates produce different interview paths.

Create both unit and API tests where practical.

==================================================
24. DEMO MODE
=============

Create a reliable DEMO_MODE.

If:

DEMO_MODE=true

the system must work without an external LLM.

Use deterministic but intelligent mock behavior.

This is important for judging.

The UI should still demonstrate:

* personalization
* adaptive questions
* follow-ups
* state
* 8+ questions
* 4+ curriculum days
* final feedback

==================================================
25. SAMPLE DEMO CANDIDATE
=========================

Use the actual candidate data.

For example, the supplied candidate profiles include candidates with very different journeys.

Do not modify candidates.json.

The application should allow selecting candidates from the provided dataset.

==================================================
-----------------------------PROMPT-2----------------------------------
You are working on my EXISTING project:

# AI Interview Agent

### "Build the interviewer, not the interview."

IMPORTANT:
Do NOT rebuild the project from scratch.

First inspect the entire existing project and understand how it currently works.

Then UPDATE and IMPROVE the existing implementation.

Preserve working functionality unless there is a strong technical reason to change it.

The goal is to make the existing project a genuinely adaptive AI technical interviewer suitable for a hackathon demonstration.

==================================================

1. FIRST: EXPLORE THE EXISTING PROJECT
   ==================================================

Before changing code, inspect:

* backend/
* frontend/
* agents/
* services/
* prompts/
* tests/
* data/
* curriculum.json
* candidates.json
* technical specification
* Docker files
* environment files
* README

Understand the current architecture and identify:

1. How interview sessions are stored.
2. How candidate profiles are analyzed.
3. How curriculum topics are selected.
4. How questions are generated.
5. How candidate answers are evaluated.
6. How follow-up questions are selected.
7. How final feedback is generated.
8. How frontend state is updated.
9. How MockProvider works.
10. How OpenAI/LLM integration works.

DO NOT modify anything until you understand the existing flow.

After inspection, implement the improvements below directly.

==================================================
2. MAIN GOAL
============

The biggest improvement needed is:

MAKE THE INTERVIEW ACTUALLY ADAPTIVE.

The current system has the architecture of an adaptive interviewer, but some parts behave too deterministically.

I want this real flow:

Candidate Profile
↓
Candidate Analyzer
↓
Interview Strategy
↓
Question
↓
Candidate Answer
↓
Answer Evaluator
↓
Follow-up Decision
↓
Next Question
↓
Update Memory
↓
Repeat
↓
Evidence-Based Feedback

The next question must depend on what the candidate actually said.

Do NOT create a fixed questionnaire.

Do NOT simply rotate through curriculum days.

==================================================
3. PRESERVE THE API CONTRACT
============================

Do NOT break the existing API.

The required endpoint is:

POST /api/interview

START:

{
"sessionId": "abc-123",
"candidate": { ...candidate.json }
}

RESPONSE:

{
"reply": "...",
"done": false
}

CONTINUATION:

{
"sessionId": "abc-123",
"message": "candidate answer"
}

FINAL:

{
"reply": "Interview completed.",
"done": true,
"feedback": {
"summary": "...",
"strengths": [],
"gaps": [],
"next": []
}
}

Keep sessionId-based state.

Do not introduce authentication.

Do not change the required response format.

==================================================
4. IMPROVE THE INTERVIEW STATE
==============================

Extend the existing session state.

It should maintain at least:

{
"sessionId": "...",
"candidate": {},
"stage": "INTRO",
"questionCount": 0,
"topicsCovered": [],
"daysCovered": [],
"questions": [],
"answers": [],
"evaluations": [],
"currentQuestion": {},
"currentTopic": {},
"currentDifficulty": "medium",
"candidateStrengths": [],
"candidateWeaknesses": [],
"followUpCount": 0,
"interviewSignals": {},
"startedAt": "...",
"completed": false
}

Every subsequent request with the same sessionId must use this state.

Never restart the interview.

==================================================
5. BUILD A REAL ANSWER EVALUATOR
================================

Improve the existing evaluator.

After every candidate answer, evaluate:

* correctness
* completeness
* technical depth
* reasoning quality
* practical understanding
* misconceptions
* missing concepts
* confidence
* ability to explain clearly

Return structured evaluation internally:

{
"score": 0-10,
"correctness": 0-10,
"depth": 0-10,
"reasoning": 0-10,
"practicality": 0-10,
"missingConcepts": [],
"misconceptions": [],
"strengths": [],
"weaknesses": [],
"recommendedAction": "...",
"followUpType": "..."
}

Possible recommended actions:

* FOLLOW_UP_DEEPER
* FOLLOW_UP_CLARIFY
* FOLLOW_UP_SCENARIO
* FOLLOW_UP_DEBUGGING
* FOLLOW_UP_TRADEOFF
* INCREASE_DIFFICULTY
* DECREASE_DIFFICULTY
* MOVE_TO_NEXT_TOPIC
* MOVE_TO_SYSTEM_DESIGN
* COMPLETE_INTERVIEW

Do not expose this internal evaluation to the candidate during the interview.

==================================================
6. BUILD A REAL FOLLOW-UP ENGINE
================================

This is the MOST IMPORTANT improvement.

The follow-up must be generated from the candidate's actual answer.

Example:

Question:
"Why are embeddings useful in a RAG system?"

Candidate:
"Embeddings convert text into vectors and allow similarity search."

The next question should NOT simply jump to another topic.

Instead:

"Good. Suppose your vector search returns documents that are semantically similar but irrelevant to the exact user question. How would you investigate and improve the retrieval pipeline?"

This is a real follow-up.

Another example:

Candidate gives an incomplete answer.

Instead of immediately changing topics:

"Can you explain what happens between creating the embedding and retrieving the nearest documents?"

Another example:

Candidate gives an excellent answer.

Increase difficulty:

"Now assume the system has 10 million documents and strict latency requirements. What changes would you make to the retrieval architecture?"

Implement this behavior.

==================================================
7. FOLLOW-UP TYPES
==================

Create a proper follow-up strategy.

### FOLLOW_UP_DEEPER

Use when the candidate is correct but shallow.

Ask about:

* implementation
* internals
* trade-offs

### FOLLOW_UP_CLARIFY

Use when the answer is vague.

Ask the candidate to explain one missing concept.

### FOLLOW_UP_SCENARIO

Give a realistic engineering scenario.

### FOLLOW_UP_DEBUGGING

Give a failure and ask how they would diagnose it.

### FOLLOW_UP_TRADEOFF

Ask them to compare two approaches.

### INCREASE_DIFFICULTY

Move from:
concept → practical → architecture → system design.

### DECREASE_DIFFICULTY

If the candidate struggles, test the underlying fundamental concept without embarrassing them.

==================================================
8. PERSONALIZATION MUST USE CANDIDATE DATA
==========================================

Use the actual candidate profile.

Analyze:

* jobRole
* yearsExperience
* education
* passed missions
* failed missions
* skipped missions
* attempts
* commitDays
* missionsCompleted
* missionsFirstTry

Create:

candidateStrengthTopics
candidateWeakTopics
candidateSkippedTopics
candidateHighAttemptTopics
candidateLowAttemptTopics
recommendedDifficulty
roleFocus

IMPORTANT:

Do not say a candidate completed something if their profile says:

* skipped
* failed
* not passed

For example, if a candidate skipped Docker/Kubernetes, do not treat Docker/Kubernetes as a demonstrated strength.

Instead, if relevant, ask a diagnostic question.

==================================================
9. USE THE CURRICULUM INTELLIGENTLY
===================================

Use the actual curriculum.json.

Do not hardcode the whole curriculum into Python.

The curriculum contains 31 days and 8 modules.

Use:

* day
* title
* objectives
* tools
* module

The next topic should be selected based on:

1. Candidate profile
2. Previous answers
3. Previous evaluation
4. Weaknesses
5. Strengths
6. Topics already covered
7. Interview stage
8. Candidate role
9. Difficulty

Do not simply select:

available_days[0]

or another deterministic first item.

==================================================
10. SMART TOPIC SELECTION
=========================

Create a scoring mechanism for candidate topic selection.

For each possible curriculum topic calculate something conceptually like:

topicScore =
relevanceToRole
+ candidateWeakness
+ candidateLearningSignal
+ previousAnswerConnection
+ curriculumImportance
+ interviewStageFit
- alreadyCoveredPenalty

Then choose the highest suitable topic.

Do not expose this calculation to the user.

Example:

If candidate answered a RAG question well:

Next could be:

* retrieval failure
* reranking
* hybrid search
* prompt grounding
* production RAG

If candidate struggles with vector databases:

Ask a targeted vector database follow-up before moving on.

==================================================
11. CROSS-TOPIC REASONING
=========================

Add questions that connect multiple curriculum days.

Examples:

Day 7 + Day 8:
"How do embeddings interact with a vector database?"

Day 8 + Day 10:
"How would you diagnose poor semantic retrieval?"

Day 10 + Day 11:
"How does retrieval quality affect RAG answer quality?"

Day 12 + Day 13:
"Why would structured outputs or function calling be preferable to free-form prompting?"

Day 20 + Day 22:
"How would conversation memory work inside a multi-agent architecture?"

Day 22 + Day 23:
"Where would MCP fit in a multi-agent system?"

Day 24 + Day 27:
"How would you secure an agentic system that can call external tools?"

Day 28 + Day 29:
"How would you monitor a deployed AI service?"

Generate these dynamically from curriculum relationships, not as a fixed script.

==================================================
12. INTERVIEW STAGES
====================

Improve the state machine:

INTRO
↓
BASELINE
↓
DEEP_DIVE
↓
CROSS_TOPIC
↓
SYSTEM_DESIGN
↓
PRODUCTION
↓
FINAL_EVALUATION
↓
COMPLETED

Do not force every candidate through every stage.

Strong candidates should reach deeper architecture questions faster.

Candidates who struggle should spend more time diagnosing fundamentals.

==================================================
13. INTERVIEW LENGTH
====================

Minimum:
8 questions.

Maximum:
15 questions.

At least:
4 different curriculum days.

However, do NOT end simply because questionCount == 8.

End when enough evidence has been collected.

Use:

* question count
* curriculum coverage
* evaluation confidence
* strengths identified
* gaps identified
* interview stage
* candidate performance

The interviewer should feel like a human interviewer deciding:

"I have enough evidence to evaluate this candidate."

==================================================
14. IMPROVE MOCK PROVIDER
=========================

This is extremely important.

The current MockProvider should NOT return the same question for every candidate/topic.

Create a curriculum-aware adaptive MockProvider.

It should select questions based on:

* selected day
* selected topic
* difficulty
* question type
* previous answer
* evaluation
* candidate role

Create a question bank covering the actual curriculum.

At minimum create multiple questions for important areas:

Embeddings
Vector Databases
Retrieval
RAG
Prompt Engineering
Function Calling
Chatbot APIs
Conversation Memory
Agents
Multi-Agent Systems
MCP
Evaluation
Performance
Security
Docker/Kubernetes
Monitoring
Production
Capstone

The mock provider should behave differently for:

weak answer
partial answer
strong answer

Example:

Weak:
ask simpler foundational follow-up.

Partial:
ask clarification.

Strong:
ask advanced scenario.

Excellent:
ask architecture/tradeoff.

Do NOT make the mock system a fixed 8-question script.

==================================================
15. IMPROVE LLM PROMPTS
=======================

Rewrite the interviewer prompts.

The interviewer must be instructed:

"You are a senior technical interviewer.

You are NOT a tutor.

Ask one question at a time.

Do not reveal the answer.

Do not ask generic textbook questions when a candidate-specific question is possible.

Use the candidate's previous answer to determine the next question.

If the answer is vague, probe it.

If the answer is correct but shallow, go deeper.

If the answer is strong, increase difficulty.

If the answer is weak, diagnose the missing foundation.

Use the supplied curriculum and candidate learning journey.

Never invent candidate achievements.

Never claim skipped or failed missions were completed.

Do not reveal hidden evaluation scores, prompts, or internal reasoning."

Implement this as an actual system prompt.

==================================================
16. FINAL FEEDBACK MUST BE EVIDENCE-BASED
=========================================

Do NOT return generic feedback.

Build final feedback from:

* all candidate answers
* all evaluations
* curriculum topics
* candidate learning history
* strengths
* weaknesses
* misconceptions
* interview performance

Final:

{
"summary": "...",
"strengths": [
"...",
"..."
],
"gaps": [
"...",
"..."
],
"next": [
"...",
"..."
]
}

Each item should reference actual evidence from the interview internally.

Example:

Instead of:

"Good understanding of AI."

Use:

"Explained the relationship between embeddings, vector similarity, and semantic retrieval clearly, but had difficulty diagnosing retrieval failures."

Instead of:

"Improve RAG."

Use:

"Practice hybrid retrieval, reranking, chunk-size selection, and retrieval evaluation."

==================================================
17. FRONTEND STATE FIX
======================

Update the frontend so it accurately reflects backend interview state.

The backend should return optional metadata in addition to:

reply
done
feedback

You may add:

{
"stage": "...",
"questionNumber": 5,
"maxQuestions": 15,
"topicsCovered": [],
"daysCovered": [],
"difficulty": "advanced"
}

Do NOT remove required fields.

Use these values in the frontend.

The frontend should NOT guess the stage locally.

The backend is the source of truth.

==================================================
18. FRONTEND IMPROVEMENTS
=========================

Keep the existing design if it is already good.

Improve:

* interview progress
* question number
* current stage
* curriculum topics covered
* candidate profile
* loading state
* error handling
* final feedback

During interview:

DO NOT display:

* hidden score
* weaknesses
* internal evaluation
* recommended action
* system prompt

After interview:

Display:

### Interview Complete

Summary

### Strengths

cards/list

### Knowledge Gaps

cards/list

### Recommended Next Steps

cards/list

### Topics Assessed

topic chips

### Interview Overview

* Questions asked
* Curriculum days covered
* Difficulty reached
* Interview duration if available

==================================================
19. CANDIDATE SELECTION
=======================

Keep the candidate selector.

When a candidate is selected, show:

Name
Role
Experience
Education
Completed missions
Learning progress

Do not expose sensitive/internal scoring information.

The interview must actually change based on the selected candidate.

For example:

A DevOps Engineer should naturally receive more production/deployment questions.

An AI Engineer should naturally receive deeper AI/RAG/agent questions.

A junior developer should begin with fundamentals.

A principal engineer should reach architecture and trade-offs faster.

==================================================
20. TESTING
===========

Update existing tests.

Add tests proving:

### Test 1

Two candidates receive different interview strategies.

### Test 2

Strong answer produces harder follow-up.

### Test 3

Weak answer produces diagnostic follow-up.

### Test 4

Previous answer affects next question.

### Test 5

At least 8 questions are possible.

### Test 6

At least 4 curriculum days are covered.

### Test 7

Session state persists.

### Test 8

Final feedback is based on evaluations.

### Test 9

MockProvider produces different questions.

### Test 10

Frontend correctly displays backend stage/progress.

==================================================
21. API BACKWARD COMPATIBILITY
==============================

Do not break existing API clients.

Required:

POST /api/interview

must continue to work.

Existing required response fields must remain:

reply
done

and final:

feedback.summary
feedback.strengths
feedback.gaps
feedback.next

Additional response metadata is allowed.

==================================================
22. DEMO MODE
=============

DEMO_MODE must work without an external API key.

Test the complete interview using DEMO_MODE.

It must demonstrate:

* candidate personalization
* adaptive questions
* follow-ups
* difficulty changes
* curriculum coverage
* session memory
* final personalized feedback

The demo should be convincing enough for a hackathon judge.

==================================================
23. DO NOT OVERENGINEER
=======================

Do NOT add unnecessary:

* databases
* authentication
* microservices
* Kubernetes complexity
* external vector databases

unless already required by the existing project.

The challenge is about the interviewer.

Focus engineering effort on:

ADAPTATION
CONTEXT
PERSONALIZATION
FOLLOW-UP REASONING
EVALUATION
FEEDBACK

==================================================
24. RUN AND VERIFY
==================

After making changes:

1. Install dependencies.
2. Start backend.
3. Start frontend.
4. Run backend tests.
5. Test POST /api/interview.
6. Start a real session.
7. Send at least 8 answers.
8. Verify different questions.
9. Verify follow-up behavior.
10. Verify 4+ curriculum days.
11. Verify final feedback.
12. Verify frontend.
13. Fix all errors.

Do not stop at "implementation complete."

Actually run and verify the project.

==================================================
25. FINAL CHECKLIST
===================

Before finishing, verify:

[ ] Existing project preserved
[ ] API still works
[ ] sessionId works
[ ] candidate personalization works
[ ] curriculum personalization works
[ ] questions are adaptive
[ ] previous answer affects next question
[ ] follow-ups are meaningful
[ ] strong answers increase difficulty
[ ] weak answers trigger diagnosis
[ ] at least 8 questions
[ ] at least 4 curriculum days
[ ] interview context persists
[ ] MockProvider is adaptive
[ ] LLM mode is adaptive
[ ] final feedback is personalized
[ ] frontend reflects real backend state
[ ] tests pass
[ ] Docker still works
[ ] README updated

==================================================
26. IMPORTANT FINAL INSTRUCTION
===============================

Do not simply explain what should be changed.

MAKE THE CHANGES DIRECTLY IN THE EXISTING PROJECT.

Do not create a second project.

Do not replace the existing application with a simplified demo.

Do not remove existing working functionality.

Inspect → modify → test → fix → verify.

The final project must demonstrate:

"Build the interviewer, not the interview."

The judge should be able to answer YES to all of these:

* Does it understand the candidate?
* Does it understand the curriculum?
* Does it remember previous answers?
* Does it ask intelligent follow-ups?
* Does it change difficulty?
* Does it probe weaknesses?
* Does it challenge strong candidates?
* Does it feel like a real technical interview?
* Does the final feedback reflect what actually happened?

Make the existing project achieve that standard.
------------------------------PROMPT-3---------------------------------
URGENT UI + INTERVIEW QUALITY FIX

I have run the existing AI Interview Agent and attached a screenshot of the current application.

DO NOT rebuild the application.

Inspect the existing code and fix the issues visible in the current running application.

CURRENT PROBLEMS OBSERVED:

1. The sidebar shows:
   "Cohort Days Covered: 0 / 31"
   even though the interview is already discussing vector search / embeddings.

2. The sidebar shows:
   "Question Progress: 1 / min 8"
   even after multiple interviewer/candidate turns.

3. The interviewer repeatedly says:
   "Thank you for that response. Let's explore the underlying trade-offs in this approach."
   This makes the interview feel scripted.

4. The interviewer sometimes generates overly long technical responses instead of asking one focused interview question.

5. The frontend state does not appear to accurately reflect backend interview state.

FIX THESE WITHOUT BREAKING THE EXISTING API.

==================================================
1. BACKEND MUST BE THE SOURCE OF TRUTH
==================================================

The frontend must NOT guess:

- question count
- stage
- curriculum days
- difficulty
- topics covered

The backend interview session already contains this information.

Return useful metadata from POST /api/interview:

{
  "reply": "...",
  "done": false,
  "stage": "DEEP_DIVE",
  "questionNumber": 3,
  "minQuestions": 8,
  "maxQuestions": 15,
  "topicsCovered": [
    "Embeddings",
    "Vector Databases"
  ],
  "daysCovered": [7, 8],
  "difficulty": "advanced"
}

For final response:

{
  "reply": "Interview completed.",
  "done": true,
  "stage": "COMPLETED",
  "questionNumber": 10,
  "topicsCovered": [...],
  "daysCovered": [...],
  "feedback": {
    "summary": "...",
    "strengths": [],
    "gaps": [],
    "next": []
  }
}

Keep the required existing fields:

reply
done
feedback.summary
feedback.strengths
feedback.gaps
feedback.next

Additional fields are allowed.

==================================================
2. FIX CURRICULUM TRACKING
==================================================

Whenever a question is generated from a curriculum day:

add that day to:

session.daysCovered

and add the topic to:

session.topicsCovered

Avoid duplicates.

Example:

Question 1:
Day 7 - Embeddings

Question 2:
Day 8 - Vector Databases

Question 3:
Day 10 - Retrieval

The frontend should display:

Cohort Days Covered: 3 / 31

and optionally:

Day 7
Day 8
Day 10

Do NOT display 0 / 31 after questions have already been asked.

==================================================
3. FIX QUESTION COUNTING
==================================================

Define clearly what counts as a question.

Only an interviewer question should increment questionCount.

Do NOT count:

- candidate answers
- loading messages
- evaluation messages
- generic acknowledgements

If the interviewer sends:

"Why would you choose HNSW over IVF?"

that increments question count.

If the candidate answers:

"HNSW is useful because..."

do NOT increment.

Make question count consistent across backend and frontend.

==================================================
4. FIX FRONTEND PROGRESS
==================================================

Remove hardcoded frontend values such as:

questionCount = 1

topicsCovered = []

stage = "BASELINE"

Instead use the values returned by the backend.

Example:

Question Progress:
3 / 8 minimum

Progress percentage:

min(questionNumber / 8, 1) * 100

If questionNumber is greater than 8, show:

9 / 8 minimum

or better:

9 questions

Do NOT make the UI confusing.

Recommended:

Question Progress
9 questions
Minimum 8

==================================================
5. MAKE THE INTERVIEWER SOUND HUMAN
==================================================

Remove repetitive generic messages such as:

"Thank you for that response. Let's explore the underlying trade-offs in this approach."

Do not use the same acknowledgement repeatedly.

The interviewer should directly react to the candidate's answer.

BAD:

Candidate:
"HNSW uses a graph structure..."

Interviewer:
"Thank you for that response. Let's explore the underlying trade-offs in this approach."

GOOD:

Candidate:
"HNSW uses a graph structure..."

Interviewer:
"You mentioned HNSW's graph structure. How would its memory cost influence your choice when the vector index contains hundreds of millions of embeddings?"

The next question must reference something from the previous answer.

==================================================
6. CREATE DYNAMIC ACKNOWLEDGEMENTS
==================================================

If an acknowledgement is needed, make it contextual.

Possible styles:

"Your explanation of HNSW's graph structure is clear."

"You correctly connected vector similarity with approximate nearest-neighbor search."

"You mentioned recall and latency; let's examine that trade-off."

"That's a reasonable approach. What happens when the retrieval results are poor?"

"Your answer covers the basic mechanism. Let's go one level deeper."

Do NOT repeat the same sentence.

Do NOT overuse acknowledgements.

Often the best response is simply the next question.

==================================================
7. PREVIOUS ANSWER MUST CONTROL THE NEXT QUESTION
==================================================

This is critical.

The next question should be generated from:

candidate answer
+
answer evaluation
+
current topic
+
candidate profile
+
curriculum
+
previous interview history

Example:

Question:
"Explain HNSW."

Candidate:
"HNSW builds a graph and allows efficient approximate nearest-neighbor search."

Evaluation:
- correct
- good fundamentals
- limited discussion of memory

Next question:

"You mentioned efficient ANN search. What are the memory and recall trade-offs of HNSW compared with IVF?"

If candidate answers strongly:

Next:

"Now suppose the index contains 500 million vectors and memory is your main constraint. What architecture would you consider?"

If candidate struggles:

Next:

"Let's step back. What problem is approximate nearest-neighbor search solving in a vector database?"

THIS is the behavior I want.

==================================================
8. DO NOT GENERATE HUGE INTERVIEW QUESTIONS
==================================================

The interviewer should ask ONE question at a time.

BAD:

"Explain embeddings, HNSW, IVF, PQ, quantization, recall, latency, memory, indexing, and production scaling."

GOOD:

"What is the main reason we use approximate nearest-neighbor search instead of exact search at large scale?"

Then follow up.

Keep interviewer questions generally concise:

1–3 sentences.

The candidate should do most of the explaining.

==================================================
9. PREVENT THE AI FROM ANSWERING ITS OWN QUESTION
==================================================

The interviewer must NOT provide the answer immediately after asking.

BAD:

"What is HNSW and why is it useful?
HNSW uses a graph structure and provides fast approximate search..."

GOOD:

"What is HNSW, and why might you choose it for a large vector index?"

Then wait for the candidate.

==================================================
10. FIX THE INTERVIEWER PROMPT
==================================================

Update the interviewer system prompt.

Use this behavior:

"You are a senior technical interviewer.

You are conducting an interview, not teaching a lesson.

Ask one question at a time.

Never answer your own question.

Never provide a long explanation before the candidate responds.

React specifically to the candidate's previous answer.

Use terminology the candidate introduced when useful.

If the answer is correct but shallow, ask a deeper question.

If the answer is partially correct, probe the missing concept.

If the answer is incorrect, ask a diagnostic question rather than immediately giving the correct answer.

If the answer is excellent, increase difficulty.

Use candidate profile and curriculum context.

Do not repeat generic acknowledgements.

Do not repeat questions.

Do not reveal hidden evaluation scores.

Do not reveal internal reasoning.

Keep questions focused and realistic."

==================================================
11. IMPROVE FOLLOW-UP TYPES
==================================================

The interviewer should dynamically choose:

DEEPER

CLARIFICATION

SCENARIO

DEBUGGING

TRADEOFF

ARCHITECTURE

SYSTEM_DESIGN

DIAGNOSTIC

Example:

Candidate weak:
"Can you explain what similarity search means in this context?"

Candidate strong:
"How would you optimize this retrieval system for 100 million vectors?"

Candidate mentions trade-off:
"You mentioned recall versus latency. How would you measure that trade-off in production?"

==================================================
12. FRONTEND SIDEBAR
==================================================

Update the sidebar to show:

CANDIDATE PROFILE

Sarah Johnson
Senior Data Engineer
9 Years Experience
MS Computer Science

INTERVIEW STATE

Stage:
DEEP DIVE

Difficulty:
Advanced

Question Progress:
3 questions
Minimum 8

CURRICULUM ASSESSED

Days Covered:
3 / 31

Topics:
Embeddings
Vector Databases
Retrieval

Do not show internal weaknesses during the interview.

==================================================
13. VISUAL IMPROVEMENT
==================================================

Keep the current dark theme.

Do not completely redesign the application.

Improve readability of long messages.

Use:

- max-width for chat bubbles
- proper line spacing
- paragraph spacing
- bullet formatting
- code formatting where appropriate
- readable technical text

Candidate answers should be visually distinct.

Interviewer questions should be easy to identify.

==================================================
14. TEST THIS EXACT SCENARIO
==================================================

Use the current candidate:

Sarah Johnson
Senior Data Engineer
9 Years Experience

Start a new session.

Question 1 should be related to her candidate profile and curriculum.

Answer with:

"Embeddings convert text into vectors so that semantically similar content can be retrieved efficiently."

Then verify that Question 2 references embeddings or retrieval.

Answer:

"I would use a vector database with approximate nearest neighbor indexing."

Verify that Question 3 becomes deeper.

Answer:

"With a very large dataset I would consider HNSW or IVF depending on the recall, memory and latency requirements."

Verify that the next question specifically probes one of those trade-offs.

The questions must NOT be identical or generic.

Verify:

daysCovered > 0

questionNumber increases correctly

stage changes correctly

difficulty changes appropriately

==================================================
15. FINAL VERIFICATION
==================================================

After implementation:

- Run backend.
- Run frontend.
- Start a fresh interview.
- Test at least 8 questions.
- Verify 4+ curriculum days.
- Verify follow-ups.
- Verify strong answer → harder question.
- Verify weak answer → diagnostic question.
- Verify frontend progress.
- Verify curriculum counter.
- Verify no repeated acknowledgement.
- Verify interviewer does not answer its own questions.
- Verify final feedback.

Do not just tell me the changes you would make.

Actually modify the existing files.

Run the application and fix errors.

Do not rebuild from scratch.
Do not create a second application.
Do not remove existing features.