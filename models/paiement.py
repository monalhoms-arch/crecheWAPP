from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Paiement:
    enfant_id: str
    montant: float
    date: datetime = datetime.now()
    mode: str = "espece"
    statut: str = "paye" # paye, en_attente
    chargily_payment_id: str = None

    def to_dict(self):
        d = asdict(self)
        return d
