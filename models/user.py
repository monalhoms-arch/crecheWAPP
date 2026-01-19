from dataclasses import dataclass, asdict
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import hashlib
import hmac
import re
import binascii

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
        try:
            return check_password_hash(self.password_hash, password)
        except ValueError as e:
            # Fallback: some stored hashes may use scrypt in the format:
            # scrypt:N:R:P$<salt_b64>$<hash_b64>
            msg = str(e)
            if self.password_hash and (self.password_hash.startswith('scrypt') or 'scrypt' in msg):
                try:
                    parts = self.password_hash.split('$')
                    method = parts[0]
                    salt_part = parts[1]
                    hash_part = parts[2]

                    # parse params if present: scrypt:N:R:P
                    params = method.split(':')
                    if len(params) >= 4:
                        n = int(params[1])
                        r = int(params[2])
                        p = int(params[3])
                    else:
                        # sensible defaults if missing
                        n, r, p = 16384, 8, 1

                    def decode_maybe_base64_or_hex(s):
                        # hex string? (only hex digits, even length)
                        if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
                            try:
                                return bytes.fromhex(s)
                            except Exception:
                                pass
                        # try base64 (add padding if needed)
                        try:
                            return base64.b64decode(s)
                        except Exception:
                            # try urlsafe base64 with padding
                            try:
                                padding = '=' * (-len(s) % 4)
                                return base64.urlsafe_b64decode(s + padding)
                            except Exception:
                                # fallback to raw bytes
                                return s.encode('utf-8')

                    salt = decode_maybe_base64_or_hex(salt_part)
                    expected = decode_maybe_base64_or_hex(hash_part)

                    # compute scrypt (may be memory-intensive for large N)
                    computed = hashlib.scrypt(password.encode('utf-8'), salt=salt, n=n, r=r, p=p, dklen=len(expected))
                    return hmac.compare_digest(computed, expected)
                except Exception:
                    return False
            raise

    def get_id(self):
        return str(self.username)  # Using username as ID for simplicity, or use _id

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
