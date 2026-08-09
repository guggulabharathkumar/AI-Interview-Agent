import json
from pathlib import Path
from typing import Dict, List, Optional
from app.config import settings
from app.models import Candidate, AnalyzedCandidateProfile

class CandidateService:
    """Service to load candidate dataset and analyze candidate profiles."""
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or settings.DATA_DIR)
        self.file_path = self.data_dir / "candidates.json"
        self._candidates: List[Candidate] = []
        self._candidate_map: Dict[str, Candidate] = {}
        self.load_candidates()

    def load_candidates(self):
        """Loads and validates candidates.json file."""
        if not self.file_path.exists():
            fallback_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "candidates.json"
            if fallback_path.exists():
                self.file_path = fallback_path
            else:
                raise FileNotFoundError(f"candidates.json not found at {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_candidates = data.get("candidates", [])
        self._candidates = [Candidate(**c) for c in raw_candidates]
        self._candidate_map = {c.member.id: c for c in self._candidates}

    def get_all_candidates(self) -> List[Candidate]:
        return self._candidates

    def get_candidate_by_id(self, candidate_id: str) -> Optional[Candidate]:
        return self._candidate_map.get(candidate_id)

    def analyze_candidate(self, candidate: Candidate) -> AnalyzedCandidateProfile:
        """Analyzes candidate missions, signals, and background to produce an internal candidate profile."""
        strength_topics: List[str] = []
        weak_topics: List[str] = []
        skipped_topics: List[str] = []
        high_attempt_topics: List[str] = []
        low_attempt_topics: List[str] = []

        for mission in candidate.missions:
            title = mission.title
            attempts = mission.attempts or 1

            if mission.skipped:
                skipped_topics.append(title)
                continue

            if mission.passed:
                if attempts == 1:
                    low_attempt_topics.append(title)
                    strength_topics.append(title)
                elif attempts >= 3:
                    high_attempt_topics.append(title)
                    weak_topics.append(title)
                else:
                    strength_topics.append(title)
            else:
                # Failed mission - strict non-completion
                weak_topics.append(title)
                if attempts >= 2:
                    high_attempt_topics.append(title)

        # Experience level classification
        yrs = candidate.member.yearsExperience
        role = candidate.member.jobRole.lower()

        if "senior" in role or "lead" in role or "principal" in role or yrs >= 8:
            exp_level = "Senior"
        elif yrs >= 3:
            exp_level = "Intermediate"
        else:
            exp_level = "Junior"

        # Role focus classification
        if any(r in role for r in ["ai", "machine learning", "data scientist", "llm"]):
            role_focus = "AI_ENGINEER"
        elif any(r in role for r in ["devops", "platform", "infrastructure", "sre", "cloud"]):
            role_focus = "DEVOPS"
        elif any(r in role for r in ["backend", "software", "systems"]):
            role_focus = "BACKEND"
        elif any(r in role for r in ["business", "analyst", "manager", "product", "ux", "marketing", "hr"]):
            role_focus = "NON_TECH"
        else:
            role_focus = "BACKEND"

        # Recommended starting difficulty based on role and experience
        if role_focus == "NON_TECH":
            rec_diff = "Beginner" if exp_level == "Junior" else "Intermediate"
        elif exp_level == "Senior":
            rec_diff = "Advanced"
        elif exp_level == "Intermediate":
            rec_diff = "Intermediate"
        else:
            rec_diff = "Beginner"

        return AnalyzedCandidateProfile(
            strengthTopics=strength_topics,
            weakTopics=weak_topics,
            skippedTopics=skipped_topics,
            highAttemptTopics=high_attempt_topics,
            lowAttemptTopics=low_attempt_topics,
            experienceLevel=exp_level,
            recommendedDifficulty=rec_diff,
            roleFocus=role_focus
        )

candidate_service = CandidateService()
