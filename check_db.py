from db import db
import datetime

print("--- CHECKING DB ---")
count = db.presences.count_documents({})
print(f"Total Presences: {count}")

all_p = list(db.presences.find())
for p in all_p:
    print(f"Record: {p}")

print("--- END CHECK ---")
