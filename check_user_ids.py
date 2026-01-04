from db import db
from bson.objectid import ObjectId

print("--- CHECKING USER _ID TYPES ---")
users = list(db.users.find())

for u in users:
    uid = u.get('_id')
    print(f"User: {u.get('username')} | _id: {uid} | Type: {type(uid)}")
