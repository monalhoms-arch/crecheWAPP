from db import db
from bson.objectid import ObjectId

print("--- AUDIT USER LINKS ---")

users = list(db.users.find())
print(f"Total Users: {len(users)}\n")

for u in users:
    role = u.get('role')
    username = u.get('username')
    related_id = u.get('related_id')
    
    status = "OK"
    details = ""
    
    if role == 'admin':
        status = "INFO"
        details = "Admin account"
    elif not related_id:
        status = "MISSING"
        details = "No related_id found"
    else:
        # Check specific collection based on role
        collection = None
        if role == 'parent':
            collection = db.parents
        elif role == 'educateur':
            collection = db.educateurs
        elif role == 'dietitian':
            collection = db.dietitians
            
        if collection is not None:
            try:
                # Try ObjectId first
                profile = collection.find_one({"_id": ObjectId(related_id)})
                if not profile:
                    # Try String
                     profile = collection.find_one({"_id": str(related_id)})
                
                if profile:
                    details = f"Linked to: {profile.get('nom', 'Unknown')}"
                else:
                    status = "BROKEN"
                    details = f"Profile not found for ID: {related_id}"
            except Exception as e:
                 status = "ERROR"
                 details = f"Invalid ID format: {e}"
        else:
            status = "UNKNOWN_ROLE"
            details = f"Role '{role}' not recognized"

    print(f"[{status}] User: {username} ({role}) -> {details}")

print("\n--- AUDIT COMPLETE ---")
