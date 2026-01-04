from db import db
from bson.objectid import ObjectId

print("--- Menus in Database ---")
menus = list(db.menus.find())
for m in menus:
    print(f"Menu: {m.get('name')}")
    meals = m.get('meals', [])
    print(f"  Meals count: {len(meals)}")
    for meal in meals:
        print(f"    Meal: {meal}")
        # Try to find the full meal
        try:
            full = db.meals.find_one({"_id": ObjectId(meal['_id'])})
            print(f"      Full Meal found: {full is not None}")
            if full:
                print(f"      Full Meal Name: {full.get('name')}")
                print(f"      Full Meal Calories: {full.get('calories')}")
        except Exception as e:
            print(f"      Error finding full meal: {e}")
