from enum import Enum
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class StageEnum(str, Enum):
    INTRO = "INTRO"
    BASELINE = "BASELINE"
    DEEP_DIVE = "DEEP_DIVE"
    CROSS_TOPIC = "CROSS_TOPIC"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"
    PRODUCTION = "PRODUCTION"
    FINAL_EVALUATION = "FINAL_EVALUATION"
    COMPLETED = "COMPLETED"

class CandidateMember(BaseModel):
    id: str
    name: str
    jobRole: str
    yearsExperience: int
    education: str
    status: Optional[str] = "COMPLETED"

class CandidateMission(BaseModel):
    day: int
    title: str
    passed: Optional[bool] = None
    skipped: Optional[bool] = None
    attempts: Optional[int] = 1

class CandidateSignals(BaseModel):
    commitDays: int
    missionsCompleted: int
    missionsFirstTry: int

class Candidate(BaseModel):
    member: CandidateMember
    missions: List[CandidateMission]
    signals: CandidateSignals

class AnalyzedCandidateProfile(BaseModel):
    strengthTopics: List[str] = Field(default_factory=list)
    weakTopics: List[str] = Field(default_factory=list)
    skippedTopics: List[str] = Field(default_factory=list)
    highAttemptTopics: List[str] = Field(default_factory=list)
    lowAttemptTopics: List[str] = Field(default_factory=list)
    experienceLevel: str = "Intermediate"
    recommendedDifficulty: str = "Intermediate"
    roleFocus: str = "BACKEND"

class CurriculumDay(BaseModel):
    day: int
    title: str
    type: str
    tools: List[str]
    objectives: List[str]

class CurriculumModule(BaseModel):
    n: int
    title: str
    days: List[int]

class CurriculumData(BaseModel):
    cohort: str
    modules: List[CurriculumModule]
    days: List[CurriculumDay]

class QuestionMetadata(BaseModel):
    question: str
    day: int
    topic: str
    difficulty: str
    type: str  # conceptual | practical | debugging | architecture | tradeoff | scenario
    purpose: str
    expectedSignals: List[str] = Field(default_factory=list)

class EvaluationResult(BaseModel):
    score: float = 7.0  # 0 to 10
    correctness: float = 7.0  # 0 to 10
    depth: float = 7.0  # 0 to 10
    reasoning: float = 7.0  # 0 to 10
    practicality: float = 7.0  # 0 to 10
    confidence: float = 7.0  # 0 to 10
    missingConcepts: List[str] = Field(default_factory=list)
    misconceptions: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendedAction: str = "FOLLOW_UP_DEEPER"
    followUpType: str = "FOLLOW_UP_DEEPER"

class FeedbackResponse(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    next: List[str]

class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[Candidate] = None
    message: Optional[str] = None

class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[FeedbackResponse] = None
    stage: Optional[str] = None
    questionNumber: Optional[int] = None
    maxQuestions: Optional[int] = 15
    topicsCovered: Optional[List[str]] = None
    daysCovered: Optional[List[int]] = None
    difficulty: Optional[str] = None
    currentTopic: Optional[str] = None

class SessionState(BaseModel):
    sessionId: str
    candidate: Candidate
    analyzedProfile: AnalyzedCandidateProfile
    stage: StageEnum = StageEnum.INTRO
    questionCount: int = 0
    topicsCovered: List[str] = Field(default_factory=list)
    daysCovered: List[int] = Field(default_factory=list)
    questions: List[QuestionMetadata] = Field(default_factory=list)
    answers: List[str] = Field(default_factory=list)
    evaluations: List[EvaluationResult] = Field(default_factory=list)
    currentQuestion: Optional[Dict[str, Any]] = None
    currentTopic: Optional[str] = None
    currentDay: Optional[int] = None
    difficulty: str = "Intermediate"
    candidateStrengths: List[str] = Field(default_factory=list)
    candidateWeaknesses: List[str] = Field(default_factory=list)
    followUpCount: int = 0
    interviewSignals: Dict[str, Any] = Field(default_factory=dict)
    startedAt: str
    completed: bool = False
    feedback: Optional[FeedbackResponse] = None
