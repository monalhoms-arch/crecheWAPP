import sys
import os
import base64
import hashlib
import binascii
from getpass import getpass

sys.path.insert(0, r'C:\Projects\gestion_creche_final')
from db import db


def make_scrypt_hash(password: str, n=32768, r=8, p=1, salt_len=12, dklen=64):
    salt = os.urandom(salt_len)
    derived = hashlib.scrypt(password.encode('utf-8'), salt=salt, n=n, r=r, p=p, dklen=dklen)
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_hex = derived.hex()
    return f"scrypt:{n}:{r}:{p}${salt_b64}${hash_hex}"


def usage():
    print('Usage: add_user_scrypt.py <username> [role] [--scrypt]')
    print('If --scrypt provided (default), the password will be hashed with scrypt (n=32768).')


def main(argv):
    if len(argv) < 2:
        usage()
        return 2

    username = argv[1]
    role = argv[2] if len(argv) >= 3 and not argv[2].startswith('--') else 'parent'
    use_scrypt = True
    if '--no-scrypt' in argv:
        use_scrypt = False

    password = None
    if len(argv) >= 4 and not argv[3].startswith('--'):
        password = argv[3]
    else:
        password = getpass('Password: ')
        confirm = getpass('Confirm: ')
        if password != confirm:
            print('Passwords do not match')
            return 3

    users = db['users']
    if users.find_one({'username': username}):
        print('User already exists:', username)
        return 4

    if use_scrypt:
        ph = make_scrypt_hash(password)
    else:
        from werkzeug.security import generate_password_hash
        ph = generate_password_hash(password)

    doc = {'username': username, 'role': role, 'password_hash': ph}
    users.insert_one(doc)
    print('Inserted user', username, 'role', role)
    print('password_hash prefix:', ph[:60])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
