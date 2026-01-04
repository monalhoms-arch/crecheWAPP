from db import db
from bson.objectid import ObjectId

target_id = "6959600e2f04fb5780f4bbb6"
print(f"Checking for Educateur with ID: {target_id}")

try:
    educ = db.educateurs.find_one({"_id": ObjectId(target_id)})
    if educ:
        print(f"FOUND: {educ['nom']} (ID: {educ['_id']})")
    else:
        print("NOT FOUND.")
except Exception as e:
    print(f"Invalid ID format: {e}")

print("\n--- All Educateurs ---")
for e in db.educateurs.find():
    print(f"- {e['nom']}: {e['_id']}")
