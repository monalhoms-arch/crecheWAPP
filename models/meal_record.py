from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class MealRecord:
    child_id: str
    date: str # YYYY-MM-DD
    meal_type: str # Breakfast, Lunch, Snack
    eaten: bool # True/False
    calories_consumed: int = 0
    comment: str = ""
    recorded_by: str = "" # Dietitian/Educateur ID
    _id: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
