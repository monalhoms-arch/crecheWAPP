from db import db
from bson.objectid import ObjectId

print("--- DEBUG EDUCATEUR GROUPS ---")

# 1. Get all Users who are Educateurs
users = list(db.users.find({"role": "educateur"}))
print(f"Found {len(users)} educateur users.")

for u in users:
    print(f"\nUser: {u['username']}")
    print(f"  related_id: {u.get('related_id')} (Type: {type(u.get('related_id'))})")
    
    if not u.get('related_id'):
        print("  -> No related_id found.")
        continue

    rid = u['related_id']
    
    # 2. Check Educateur collection
    try:
        educ = db.educateurs.find_one({"_id": ObjectId(rid)})
        print(f"  -> Linked Profile found: {educ['nom'] if educ else 'None'}")
    except Exception as e:
        print(f"  -> Error looking up profile: {e}")

    # 3. Check Groups for this ID (String)
    groups_str = list(db.groups.find({"educateur_id": str(rid)}))
    print(f"  -> Groups (by String ID): {len(groups_str)}")
    for g in groups_str:
        print(f"     - {g['nom']} (ID: {g['_id']})")

    # 4. Check Groups for this ID (ObjectId)
    try:
        groups_obj = list(db.groups.find({"educateur_id": ObjectId(rid)}))
        print(f"  -> Groups (by ObjectId): {len(groups_obj)}")
        for g in groups_obj:
            print(f"     - {g['nom']} (ID: {g['_id']})")
    except:
         print(f"  -> Groups (by ObjectId): Invalid ID format")

print("\n--- ALL GROUPS ---")
for g in db.groups.find():
    print(f"Group: {g.get('nom')}, Educateur_ID: {g.get('educateur_id')} (Type: {type(g.get('educateur_id'))})")
