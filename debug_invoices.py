from db import db
from bson.objectid import ObjectId

print("--- Children in Database ---")
enfants = list(db.enfants.find())
enfant_names = []
for e in enfants:
    print(f"Child: {e.get('nom')}, Parent ID: {e.get('parent_id')}")
    enfant_names.append(e.get('nom'))

print("\n--- Invoices in Database ---")
invoices = list(db.invoices.find())
for i in invoices:
    print(f"Invoice: {i.get('invoice_number')}, Child Name: {i.get('child_name')}, Amount: {i.get('amount')}")
    if i.get('child_name') not in enfant_names:
        print(f"  Warning: Child Name '{i.get('child_name')}' not found in enfant records!")
