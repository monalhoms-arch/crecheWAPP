from dataclasses import dataclass, asdict
from typing import Optional, List
from datetime import datetime

@dataclass
class Meal:
    name: str
    type: str # 'Breakfast', 'Lunch', 'Snack'
    calories: int = 0
    ingredients: str = ""
    nutrition_values: str = ""
    _id: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Menu:
    name: str # e.g. "Semaine 1"
    start_date: str
    end_date: str
    description: str = ""
    meals: List[dict] = None # List of Meal dicts or IDs
    _id: Optional[str] = None

    def __post_init__(self):
        if self.meals is None:
            self.meals = []

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class NutritionPlan:
    child_id: str
    goal: str
    restrictions: str
    notes: str = ""
    assigned_by: str = "" # Dietitian ID
    _id: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
