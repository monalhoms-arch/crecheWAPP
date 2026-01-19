import sys
import getpass
from werkzeug.security import generate_password_hash
from db import db


def usage():
    print("Usage: reset_user_password.py <username> [new_password]")
    print("If new_password is omitted, you will be prompted to enter it.")


def main(argv):
    if len(argv) < 2:
        usage()
        return 2

    username = argv[1]
    if len(argv) >= 3:
        new_password = argv[2]
    else:
        new_password = getpass.getpass("New password: ")
        confirm = getpass.getpass("Confirm password: ")
        if new_password != confirm:
            print("Passwords do not match.")
            return 3

    users = db['users']
    user = users.find_one({'username': username})
    if not user:
        print(f"User not found: {username}")
        return 4

    new_hash = generate_password_hash(new_password)
    users.update_one({'_id': user['_id']}, {'$set': {'password_hash': new_hash}})
    print(f"Password for user '{username}' has been reset.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
