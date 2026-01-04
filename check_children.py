from db import db

print("--- CHECKING CHILDREN ---")
count = db.enfants.count_documents({})
print(f"Total Children: {count}")

children = list(db.enfants.find())
for c in children:
    print(f"Child: {c.get('nom')} (ID: {c.get('_id')})")
print("--- END CHECK ---")
