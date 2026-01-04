from db import db

print("--- FIXING CHILDREN ---")

# Try to find record with no _id or _id is None
bad_records = list(db.enfants.find({"_id": None}))
print(f"Found {len(bad_records)} records with _id=None")

if bad_records:
    result = db.enfants.delete_many({"_id": None})
    print(f"Deleted {result.deleted_count} records with _id=None")

# Also find by name 'faisal' just in case
faisal = db.enfants.find_one({"nom": "faisal"})
if faisal:
    print(f"Check 'faisal': ID={faisal.get('_id')}")
    if faisal.get('_id') is None:
        db.enfants.delete_one({"nom": "faisal"})
        print("Deleted 'faisal' because ID is None")

print("--- END FIX ---")
