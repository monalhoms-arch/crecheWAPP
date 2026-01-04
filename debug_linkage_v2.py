from db import db
from bson.objectid import ObjectId

print("--- Linkage Audit ---")
print("\n[Users (Parents)]")
parents = list(db.users.find({'role': 'parent'}))
for p in parents:
    rid = p.get('related_id')
    print(f"User: {p['username']}, related_id: {rid} ({type(rid)})")

print("\n[Enfants]")
enfants = list(db.enfants.find())
for e in enfants:
    pid = e.get('parent_id')
    print(f"Child: {e['nom']}, parent_id: {pid} ({type(pid)})")
