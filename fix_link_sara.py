from db import db
from bson.objectid import ObjectId

username = "sara"
related_id = "6959661689142937b8de8c19"

print(f"Linking User '{username}' to Profile ID '{related_id}'...")

result = db.users.update_one(
    {"username": username},
    {"$set": {"related_id": related_id}}
)

if result.modified_count > 0:
    print("SUCCESS: Link established.")
else:
    print("WARNING: No changes made (User not found or already linked).")

# Verify
u = db.users.find_one({"username": username})
print(f"User '{u['username']}' related_id is now: {u.get('related_id')}")
