from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@dataclass
class Invoice:
    invoice_number: str
    amount: float
    child_name: str
    parent_name: str
    date: str = ""
    status: str = "PAID"
    _id: Optional[str] = None

    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

    def generate_pdf(self):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "FACTURE / INVOICE")
        c.drawString(100, 730, "-----------------")
        c.drawString(100, 700, f"Numéro: {self.invoice_number}")
        c.drawString(100, 680, f"Date: {self.date}")
        c.drawString(100, 660, f"Parent: {self.parent_name}")
        c.drawString(100, 640, f"Enfant: {self.child_name}")
        c.drawString(100, 600, f"Montant: {self.amount} EUR")
        c.drawString(100, 580, f"Statut: {self.status}")
        c.save()
        buffer.seek(0)
        return buffer
