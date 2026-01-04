from dataclasses import dataclass, asdict
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class User(UserMixin):
    username: str
    role: str  # 'admin', 'parent', 'educateur', 'dietitian'
    password_hash: str = ""
    _id: Optional[str] = None
    related_id: Optional[str] = None  # ID of the Parent or Educateur profile

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.username)  # Using username as ID for simplicity, or use _id

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
