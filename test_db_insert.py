from db import db
import datetime

print("--- START DB TEST ---")

# 1. Check current count
count_before = db.presences.count_documents({})
print(f"Count Before: {count_before}")

# 2. Try Insert
test_doc = {
    "enfant_id": "TEST_ID",
    "nom_enfant": "TEST_CHILD",
    "date": "2025-01-01",
    "statut": "present",
    "timestamp": datetime.datetime.now()
}
try:
    result = db.presences.insert_one(test_doc)
    print(f"Insert Result ID: {result.inserted_id}")
except Exception as e:
    print(f"INSERT ERROR: {e}")

# 3. Check count again
count_after = db.presences.count_documents({})
print(f"Count After: {count_after}")

# 4. Read back
found = db.presences.find_one({"_id": result.inserted_id})
print(f"Read Back: {found}")

# 5. Clean up
db.presences.delete_one({"_id": result.inserted_id})
print("Cleaned up test record.")

print("--- END DB TEST ---")
