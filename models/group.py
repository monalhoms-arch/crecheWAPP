from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Group:
    nom: str
    capacity: int
    age_range: str
    educateur_id: Optional[str] = None
    _id: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
