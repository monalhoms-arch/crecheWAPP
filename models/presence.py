from dataclasses import dataclass, asdict

@dataclass
class Presence:
    enfant_id: str
    nom_enfant: str
    date: str
    statut: str

    def to_dict(self):
        return asdict(self)
