from db import db
from models.user import User

# Create a test user
test_user = User(username="test_delete", role="admin")
test_user.set_password("test123")

result = db.users.insert_one(test_user.to_dict())
print(f"Created test user with ID: {result.inserted_id}")
print(f"Type: {type(result.inserted_id)}")

# Verify
u = db.users.find_one({"_id": result.inserted_id})
print(f"Verification: {u['username']} exists with _id: {u['_id']}")
