from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Enfant:
    nom: str
    age: int
    code: str = ""
    gender: str = "" # 'M' or 'F'
    allergies: list = None # List of strings
    group_id: Optional[str] = None
    parent_id: Optional[str] = None
    _id: Optional[str] = None

    def __post_init__(self):
        if self.allergies is None:
            self.allergies = []

    def to_dict(self):
        d = asdict(self)
        if d.get('_id') is None:
            del d['_id']
        return d
