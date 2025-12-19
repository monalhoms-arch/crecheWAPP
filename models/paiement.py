from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Paiement:
    enfant_id: str
    montant: float
    date: datetime = datetime.now()
    mode: str = "espece"

    def to_dict(self):
        d = asdict(self)
        return d
