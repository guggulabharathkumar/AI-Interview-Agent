FEEDBACK_SYSTEM_PROMPT = """You are an expert AI interview panel reviewer.
Synthesize the overall candidate performance across the entire technical interview into actionable, constructive feedback.

JSON Structure Required:
{
  "summary": "A concise paragraph (2-3 sentences) summarizing overall performance, technical depth, and readiness.",
  "strengths": ["Concise, specific technical bullet point 1", "Point 2", "Point 3"],
  "gaps": ["Concise, specific technical gap 1", "Gap 2"],
  "next": ["Actionable, concrete recommendation 1", "Recommendation 2", "Recommendation 3"]
}

Guidelines:
- Feedback MUST be directly grounded in the actual questions asked, candidate answers, and evaluation logs.
- Do NOT provide generic platitudes. Reference specific curriculum topics covered (e.g. RAG, Embeddings, Multi-Agent Orchestration, Docker, Prompt Engineering).
- Keep bullet points clear, technical, and actionable.
- Return ONLY strictly valid JSON.
"""

def build_feedback_user_prompt(
    candidate_name: str,
    candidate_role: str,
    questions: list,
    answers: list,
    evaluations: list,
    topics_covered: list
) -> str:
    transcript_text = ""
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        q_text = q.question if hasattr(q, "question") else q.get("question", "")
        eval_score = evaluations[i-1].score if i-1 < len(evaluations) and hasattr(evaluations[i-1], "score") else "N/A"
        transcript_text += f"\nTurn {i} (Topic: {getattr(q, 'topic', '')}):\nQ: {q_text}\nA: {a}\nEval Score: {eval_score}\n"

    return f"""Candidate Name: {candidate_name}
Target Role: {candidate_role}
Topics Covered: {topics_covered}

Interview Transcript & Evaluations:
{transcript_text}

Generate the final structured JSON feedback now.
"""
