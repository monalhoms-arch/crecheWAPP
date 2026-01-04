from db import db
from pprint import pprint

print("--- PRESENCES IN DB ---")
presences = list(db.presences.find())
print(f"Total count: {len(presences)}")
for p in presences:
    pprint(p)
print("--- END ---")
