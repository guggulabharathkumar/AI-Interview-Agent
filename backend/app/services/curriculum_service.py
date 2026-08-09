import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from app.config import settings
from app.models import CurriculumData, CurriculumDay, CurriculumModule, AnalyzedCandidateProfile, StageEnum

class CurriculumService:
    """Service to load, index, query curriculum data and perform smart topic scoring."""
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or settings.DATA_DIR)
        self.file_path = self.data_dir / "curriculum.json"
        self._curriculum: Optional[CurriculumData] = None
        self._day_map: Dict[int, CurriculumDay] = {}
        self.load_curriculum()

    def load_curriculum(self):
        """Loads and validates curriculum.json file."""
        if not self.file_path.exists():
            fallback_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "curriculum.json"
            if fallback_path.exists():
                self.file_path = fallback_path
            else:
                raise FileNotFoundError(f"curriculum.json not found at {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._curriculum = CurriculumData(**data)
        self._day_map = {d.day: d for d in self._curriculum.days}

    def get_curriculum(self) -> CurriculumData:
        return self._curriculum

    def get_day(self, day_num: int) -> Optional[CurriculumDay]:
        return self._day_map.get(day_num)

    def get_all_days(self) -> List[CurriculumDay]:
        return self._curriculum.days if self._curriculum else []

    def select_smart_topic(
        self,
        profile: AnalyzedCandidateProfile,
        stage: StageEnum,
        days_covered: List[int],
        last_answer: str = "",
        last_eval_score: float = 7.0
    ) -> CurriculumDay:
        """Implements smart topic scoring mechanism to select optimal curriculum day."""
        all_days = self.get_all_days()
        best_day = all_days[0]
        best_score = -9999.0

        for c_day in all_days:
            day_num = c_day.day
            title = c_day.title
            title_lower = title.lower()

            # 1. Already covered penalty
            already_covered_penalty = 200.0 if day_num in days_covered else 0.0

            # 2. Relevance to Role
            relevance_to_role = 0.0
            if profile.roleFocus == "AI_ENGINEER":
                if day_num in [7, 8, 10, 11, 12, 13, 21, 22, 23, 25]:
                    relevance_to_role = 30.0
            elif profile.roleFocus == "DEVOPS":
                if day_num in [1, 2, 3, 16, 24, 27, 28, 29, 30]:
                    relevance_to_role = 30.0
            elif profile.roleFocus == "BACKEND":
                if day_num in [3, 4, 5, 8, 10, 13, 16, 18, 20]:
                    relevance_to_role = 30.0
            elif profile.roleFocus == "NON_TECH":
                if day_num in [1, 3, 6, 7, 12, 16, 20, 31]:
                    relevance_to_role = 30.0

            # 3. Candidate Weakness & Failure Probing Signal
            candidate_weakness = 0.0
            if title in profile.weakTopics or title in profile.highAttemptTopics:
                candidate_weakness = 25.0

            # 4. Candidate Learning Signal (strength baseline)
            candidate_signal = 0.0
            if title in profile.strengthTopics:
                candidate_signal = 15.0

            # 5. Connection to previous answer
            previous_conn = 0.0
            if last_answer:
                last_lower = last_answer.lower()
                for tool in c_day.tools:
                    if tool.lower() in last_lower:
                        previous_conn += 10.0

            # 6. Stage Fit
            stage_fit = 0.0
            if stage == StageEnum.BASELINE:
                if day_num in [7, 8, 10, 12]:
                    stage_fit = 40.0
            elif stage == StageEnum.DEEP_DIVE:
                if day_num in [8, 10, 11, 13, 16, 18, 20]:
                    stage_fit = 40.0
            elif stage == StageEnum.CROSS_TOPIC:
                if day_num in [10, 11, 13, 20, 22, 23]:
                    stage_fit = 40.0
            elif stage == StageEnum.SYSTEM_DESIGN:
                if day_num in [16, 21, 22, 23, 24]:
                    stage_fit = 40.0
            elif stage in [StageEnum.PRODUCTION, StageEnum.FINAL_EVALUATION]:
                if day_num in [25, 27, 28, 29, 30, 31]:
                    stage_fit = 40.0

            # Total Topic Score calculation
            total_score = (
                relevance_to_role
                + candidate_weakness
                + candidate_signal
                + previous_conn
                + stage_fit
                - already_covered_penalty
            )

            if total_score > best_score:
                best_score = total_score
                best_day = c_day

        return best_day

    def get_cross_topic_pairing(self, primary_day: int) -> Tuple[int, str]:
        """Returns dynamic cross-topic pairing title connecting two curriculum concepts."""
        pairings = {
            7: (8, "Embeddings → Vector Database Indexing"),
            8: (10, "Vector DB → Semantic Retrieval Engine"),
            10: (11, "Retrieval Engine → RAG Context Grounding"),
            12: (13, "Prompt Engineering → Function Calling & Structured Outputs"),
            16: (20, "Backend API → Conversation Context Management"),
            20: (22, "Conversation Memory → Multi-Agent Orchestration"),
            22: (23, "Multi-Agent Systems → Model Context Protocol (MCP) Tools"),
            24: (27, "Agent Tool Execution → Security & Injection Protection"),
            28: (29, "Docker Deployment → Production Monitoring & Observability")
        }
        return pairings.get(primary_day, (primary_day + 1, "Cross-Topic Synthesis"))

curriculum_service = CurriculumService()
