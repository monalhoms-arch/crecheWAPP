from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Activite:
    titre: str
    description: Optional[str] = ""
    date: Optional[str] = ""

    def to_dict(self):
        return asdict(self)
