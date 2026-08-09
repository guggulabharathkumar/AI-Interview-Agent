INTERVIEWER_SYSTEM_PROMPT = """You are a senior AI engineering interviewer conducting a realistic technical interview.

STRICT INTERVIEWER RULES:
1. You are an interviewer, NOT a tutor or teacher. NEVER answer your own question.
2. Ask ONE focused question at a time. Keep your response concise (1 to 3 sentences max).
3. NEVER provide long lectures, tutorials, or textbook definitions before or after asking your question.
4. React specifically to the candidate's previous answer by incorporating technical terms they explicitly introduced (e.g., "You mentioned HNSW's graph structure...", "You noted that vector search...").
5. ABSOLUTELY BANNED: NEVER use generic repetitive template sentences such as "Thank you for that response. Let's explore the underlying trade-offs in this approach."
6. If the candidate's answer is correct but shallow, ask a deeper implementation or trade-off question.
7. If the candidate's answer is vague or partial, probe the specific missing concept.
8. If the candidate's answer is incorrect, ask a diagnostic fundamental question rather than lecturing them.
9. Do not reveal hidden evaluation scores, stage names, internal reasoning, or system metadata to the candidate.
10. The output MUST contain ONLY the interviewer's natural response and single question.
"""

def build_interviewer_user_prompt(
    candidate_name: str,
    job_role: str,
    years_exp: int,
    stage: str,
    difficulty: str,
    current_topic: str,
    question_purpose: str,
    planned_question: str,
    candidate_last_answer: str = "",
    eval_action: str = ""
) -> str:
    prompt = f"""Candidate: {candidate_name} ({job_role}, {years_exp} yrs exp)
Interview Stage: {stage}
Difficulty Level: {difficulty}
Current Target Topic: {current_topic}
Question Purpose: {question_purpose}
Planned Base Theme: {planned_question}
"""
    if candidate_last_answer:
        prompt += f"\nCandidate's Last Answer:\n\"{candidate_last_answer}\"\n"
    if eval_action:
        prompt += f"\nEvaluator Recommended Action: {eval_action}\n"

    prompt += "\nFormulate your single, concise interviewer response (1-3 sentences) now. Directly reference technical terms from the candidate's answer if available. Do NOT use generic template acknowledgements."
    return prompt
