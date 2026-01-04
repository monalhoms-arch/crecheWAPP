from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Dietitian:
    nom: str
    telephone: str = ""
    email: str = ""
    specialite: str = "Général"
    _id: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
