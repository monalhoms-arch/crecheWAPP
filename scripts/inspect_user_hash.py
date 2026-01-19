import sys
import re
import base64

sys.path.insert(0, r'C:\Projects\gestion_creche_final')
from db import db

def decode_maybe_base64_or_hex(s):
    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        try:
            return bytes.fromhex(s)
        except Exception:
            pass
    try:
        return base64.b64decode(s)
    except Exception:
        try:
            padding = '=' * (-len(s) % 4)
            return base64.urlsafe_b64decode(s + padding)
        except Exception:
            return s.encode('utf-8')

def main():
    if len(sys.argv) < 2:
        print('Usage: inspect_user_hash.py <username>')
        return 2
    username = sys.argv[1]
    u = db['users'].find_one({'username': username})
    if not u:
        print('user not found:', username)
        return 3
    h = u.get('password_hash','')
    print('username:', username)
    print('stored_hash:', h)
    parts = h.split('$')
    print('parts count:', len(parts))
    for i,p in enumerate(parts):
        print(i, p[:200])
    if len(parts) >= 3:
        salt = decode_maybe_base64_or_hex(parts[1])
        expected = decode_maybe_base64_or_hex(parts[2])
        print('salt hex:', salt.hex(), 'len', len(salt))
        print('expected hex prefix:', expected.hex()[:128], 'len', len(expected))
    return 0

if __name__ == '__main__':
    sys.exit(main())
