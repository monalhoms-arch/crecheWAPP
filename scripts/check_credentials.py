import sys

def main(argv):
    if len(argv) < 3:
        print("Usage: check_credentials.py <username> <password>")
        return 2

    username = argv[1]
    password = argv[2]

    # ensure project root on path
    sys.path.insert(0, r'C:\Projects\gestion_creche_final')

    from db import db
    from models.user import User

    users = db['users']
    user = users.find_one({'username': username})
    if not user:
        print(f"User not found: {username}")
        return 3

    print('stored_hash prefix:', user.get('password_hash', '')[:80])
    obj = User(username=user['username'], role=user['role'], password_hash=user.get('password_hash',''), _id=str(user['_id']), related_id=user.get('related_id'))
    try:
        ok = obj.check_password(password)
    except Exception as e:
        print('check_password raised exception:', repr(e))
        ok = False

    print('password valid:', ok)
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
