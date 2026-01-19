import base64
import re

s = "scrypt:32768:8:1$hqveTXWeoWsKlfaB$f9dcd329ed57a9b4e452912ecabfca1c6836b410de44a129d93f5b70ce7823abc9213fd858c40ddf2cd02225bdcf0ef219ff9331ccac3eac769a47f91d85b853"

parts = s.split('$')
method, salt_part, hash_part = parts[0], parts[1], parts[2]

print('method:', method)


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
        try:
            padding = '=' * (-len(s) % 4)
            return base64.urlsafe_b64decode(s + padding)
        except Exception:
            return s.encode('utf-8')

salt = decode_maybe_base64_or_hex(salt_part)
expected = decode_maybe_base64_or_hex(hash_part)

print('salt (hex):', salt.hex())
print('salt_len:', len(salt))
print('expected (hex prefix):', expected.hex()[:64])
print('expected_len:', len(expected))
