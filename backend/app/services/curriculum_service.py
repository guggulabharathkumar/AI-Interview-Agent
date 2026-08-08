import json
from pathlib import Path
from typing import Dict, List, Optional
from app.config import settings
from app.models import CurriculumData, CurriculumDay, CurriculumModule

class CurriculumService:
    """Service to load, index, and query curriculum data."""
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or settings.DATA_DIR)
        self.file_path = self.data_dir / "curriculum.json"
        self._curriculum: Optional[CurriculumData] = None
        self._day_map: Dict[int, CurriculumDay] = {}
        self.load_curriculum()

    def load_curriculum(self):
        """Loads and validates curriculum.json file."""
        if not self.file_path.exists():
            # Try workspace root fallback
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

    def get_module_for_day(self, day_num: int) -> Optional[CurriculumModule]:
        if not self._curriculum:
            return None
        for mod in self._curriculum.modules:
            if day_num in mod.days:
                return mod
            # Check range if days list is start/end range
            if len(mod.days) == 2 and mod.days[0] <= day_num <= mod.days[1]:
                return mod
        return None

    def get_days_by_numbers(self, day_nums: List[int]) -> List[CurriculumDay]:
        return [self._day_map[d] for d in day_nums if d in self._day_map]

curriculum_service = CurriculumService()
