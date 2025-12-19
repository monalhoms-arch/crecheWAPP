from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Parent:
    nom: str
    telephone: Optional[str] = ""
    email: Optional[str] = ""
    created_at: datetime = datetime.now()

    def to_dict(self):
        return asdict(self)
