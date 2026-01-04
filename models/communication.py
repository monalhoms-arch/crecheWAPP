from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Message:
    sender_id: str # Username or User ID
    recipient_id: str # Username or User ID
    subject: str
    body: str
    timestamp: str = ""
    read: bool = False
    _id: Optional[str] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Complaint:
    parent_id: str # Username or User ID
    title: str
    description: str
    status: str = "PENDING" # PENDING, RESOLVED, CLOSED
    timestamp: str = ""
    response: str = ""
    _id: Optional[str] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
