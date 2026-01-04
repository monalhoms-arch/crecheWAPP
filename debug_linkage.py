from db import db
from bson.objectid import ObjectId

print("--- Current User Context (Faysal's Parent) ---")
# Assuming the user is faysal_parent or similar
parent_user = db.users.find_one({"username": "aziz"}) # Aziz is likely the parent
if parent_user:
    rid = parent_user.get('related_id')
    print(f" Aziz related_id: '{rid}' (Type: {type(rid)})")
else:
    print("aziz user not found")

print("\n--- Children Check ---")
child = db.enfants.find_one({"nom": "faysal"})
if child:
    pid = child.get('parent_id')
    print(f" faysal parent_id: '{pid}' (Type: {type(pid)})")
    
    # Try finding with both types
    if rid:
        found_str = db.enfants.find_one({"parent_id": str(rid)})
        found_obj = None
        try:
            found_obj = db.enfants.find_one({"parent_id": ObjectId(rid)})
        except: pass
        
        print(f" Match with STRING: {found_str is not None}")
        print(f" Match with OBJECTID: {found_obj is not None}")
else:
    print("faysal child not found")
