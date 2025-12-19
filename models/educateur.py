from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Educateur:
    nom: str
    specialite: Optional[str] = ""

    def to_dict(self):
        return asdict(self)
