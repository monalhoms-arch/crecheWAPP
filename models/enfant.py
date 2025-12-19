from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Enfant:
    nom: str
    age: int
    parent_id: Optional[str] = None

    def to_dict(self):
        return asdict(self)
