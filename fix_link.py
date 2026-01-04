from db import db
from bson.objectid import ObjectId

username = "fati"
educateur_id = "6959600e2f04fb5780f4bbb6"

print(f"Linking User '{username}' to Educateur ID '{educateur_id}'...")

result = db.users.update_one(
    {"username": username},
    {"$set": {"related_id": educateur_id}}
)

if result.modified_count > 0:
    print("SUCCESS: Link established.")
else:
    print("WARNING: No changes made (User not found or already linked).")

# Verify
u = db.users.find_one({"username": username})
print(f"User '{u['username']}' related_id is now: {u.get('related_id')}")
