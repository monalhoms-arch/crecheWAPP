from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from flask_login import current_user, login_required
from db import db
from models.nutrition import Meal, Menu, NutritionPlan
from utils.decorators import role_required

nutrition_bp = Blueprint("nutrition_bp", __name__, template_folder="../templates")

@nutrition_bp.route("/meals", methods=["GET", "POST"])
@role_required(['dietitian'])
def manage_meals():
    if request.method == "POST":
        name = request.form.get("name")
        m_type = request.form.get("type")
        calories = int(request.form.get("calories", 0)) if request.form.get("calories") else 0
        ingredients = request.form.get("ingredients", "")
        if name:
            m = Meal(name=name, type=m_type, calories=calories, ingredients=ingredients)
            db.meals.insert_one(m.to_dict())
            flash(f"Repas '{name}' ajouté", "success")
        return redirect(url_for("nutrition_bp.manage_meals"))
    
    meals = list(db.meals.find().sort("_id", -1))
    for m in meals:
        m['_id'] = str(m['_id'])
    return render_template("nutrition/meals.html", meals=meals)

@nutrition_bp.route("/meals/edit/<id>", methods=["POST"])
@role_required(['dietitian'])
def edit_meal(id):
    try:
        name = request.form.get("name")
        m_type = request.form.get("type")
        calories = int(request.form.get("calories", 0)) if request.form.get("calories") else 0
        ingredients = request.form.get("ingredients", "")
        
        db.meals.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": name,
                "type": m_type,
                "calories": calories,
                "ingredients": ingredients
            }}
        )
        flash(f"Repas '{name}' modifié", "success")
    except Exception as e:
        flash(f"Erreur lors de la modification: {str(e)}", "error")
    return redirect(url_for("nutrition_bp.manage_meals"))

@nutrition_bp.route("/meals/delete/<id>")
@role_required(['dietitian'])
def delete_meal(id):
    try:
        meal = db.meals.find_one({"_id": ObjectId(id)})
        db.meals.delete_one({"_id": ObjectId(id)})
        flash(f"Repas '{meal['name']}' supprimé", "info")
    except Exception as e:
        flash(f"Erreur lors de la suppression: {str(e)}", "error")
    return redirect(url_for("nutrition_bp.manage_meals"))

@nutrition_bp.route("/menus", methods=["GET", "POST"])
@login_required # Parents can view (filtered logic needed later), Dietitian manage
def manage_menus():
    if request.method == "POST":
        if current_user.role != 'dietitian':
            return "Unauthorized", 403
            
        name = request.form.get("name")
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        # Simplified: Selecting meal IDs to add to menu
        meal_ids = request.form.getlist("meal_ids") 
        
        selected_meals = []
        if meal_ids:
             # Fetch minimal meal info
             selected_meals = list(db.meals.find({"_id": {"$in": [ObjectId(mid) for mid in meal_ids]}}, {"name":1, "type":1}))
             # Convert ObjectIds to str for data class
             for sm in selected_meals:
                 sm['_id'] = str(sm['_id'])

        if name:
            menu = Menu(name=name, start_date=start, end_date=end, meals=selected_meals)
            db.menus.insert_one(menu.to_dict())
        return redirect(url_for("nutrition_bp.manage_menus"))

    menus = list(db.menus.find().sort("start_date", -1))
    
    # Convert ObjectId to string for JSON serialization
    for menu in menus:
        menu['_id'] = str(menu['_id'])
        # Enrich meals with full data from db.meals
        enriched_meals = []
        for m_brief in menu.get('meals', []):
            full_meal = db.meals.find_one({"_id": ObjectId(m_brief['_id'])})
            if full_meal:
                full_meal['_id'] = str(full_meal['_id'])
                enriched_meals.append(full_meal)
            else:
                enriched_meals.append(m_brief)
        menu['meals'] = enriched_meals
    
    # Fetch all meals for the form and stringify their IDs
    meals = list(db.meals.find())
    for m in meals:
        m['_id'] = str(m['_id'])
        
    return render_template("nutrition/menus.html", menus=menus, meals=meals)

@nutrition_bp.route("/plans/<child_id>", methods=["GET", "POST"])
@login_required
def child_nutrition_plan(child_id):
    # Check access: Admin/Dietitian or Parent of this child
    child = db.enfants.find_one({"_id": ObjectId(child_id)})
    if not child:
        return "Child not found", 404

    if current_user.role == 'parent':
        # Verify parent owns child
        if not current_user.related_id:
             return "Parent profile not linked", 403
        # Assuming child has parent_id or checking via list logic
        if str(child.get('parent_id')) != current_user.related_id: # Direct check if parent_id stored on child
             # Fallback check if simple string match isn't enough (e.g. if one uses specific logic)
             return "Unauthorized", 403
    
    # Logic for POST (Update Plan) - Only Dietitian
    if request.method == "POST":
        if current_user.role != 'dietitian':
            return "Unauthorized to edit", 403
            
        goal = request.form.get("goal")
        restrictions = request.form.get("restrictions")
        notes = request.form.get("notes")
        
        plan = NutritionPlan(
            child_id=child_id,
            goal=goal,
            restrictions=restrictions,
            notes=notes,
            assigned_by=current_user.username
        )
        # Upsert
        db.nutrition_plans.update_one(
            {"child_id": child_id},
            {"$set": plan.to_dict()},
            upsert=True
        )
        return redirect(url_for("nutrition_bp.child_nutrition_plan", child_id=child_id))

    current_plan = db.nutrition_plans.find_one({"child_id": child_id})
    # Fetch meal records
    records = list(db.meal_records.find({"child_id": child_id}).sort("date", -1))
    return render_template("nutrition/plan.html", child=child, plan=current_plan, records=records)

@nutrition_bp.route("/log_meal/<child_id>", methods=["POST"])
@role_required(['dietitian', 'educateur']) # Educators can also log what child ate
def log_meal(child_id):
    date = request.form.get("date")
    meal_type = request.form.get("meal_type")
    eaten = request.form.get("eaten") == 'on'
    comment = request.form.get("comment")
    
    from models.meal_record import MealRecord
    rec = MealRecord(
        child_id=child_id,
        date=date,
        meal_type=meal_type,
        eaten=eaten,
        comment=comment,
        recorded_by=current_user.username
    )
    db.meal_records.insert_one(rec.to_dict())
    return redirect(url_for("nutrition_bp.child_nutrition_plan", child_id=child_id))

@nutrition_bp.route("/menus/edit/<id>", methods=["POST"])
@role_required(['dietitian'])
def edit_menu(id):
    try:
        menu_to_edit = db.menus.find_one({"_id": ObjectId(id)})
        if not menu_to_edit:
            flash("Menu introuvable", "error")
            return redirect(url_for("nutrition_bp.manage_menus"))
        
        name = request.form.get("name")
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        meal_ids = request.form.getlist("meal_ids")
        
        selected_meals = []
        if meal_ids:
            # Store only ID, name, and type in the menu document (brief version)
            db_meals = list(db.meals.find({"_id": {"$in": [ObjectId(mid) for mid in meal_ids]}}, {"name":1, "type":1}))
            for sm in db_meals:
                sm['_id'] = str(sm['_id'])
                selected_meals.append(sm)
        
        update_data = {
            "name": name,
            "start_date": start,
            "end_date": end,
            "meals": selected_meals
        }
        
        db.menus.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        flash(f"Menu '{name}' modifié avec succès", "success")
        
    except Exception as e:
        flash(f"Erreur lors de la modification: {str(e)}", "error")
    
    return redirect(url_for("nutrition_bp.manage_menus"))

@nutrition_bp.route("/menus/delete/<id>", methods=["GET", "POST"])
@role_required(['dietitian'])
def delete_menu(id):
    try:
        menu_to_delete = db.menus.find_one({"_id": ObjectId(id)})
        if not menu_to_delete:
            flash("Menu introuvable", "error")
            return redirect(url_for("nutrition_bp.manage_menus"))
        
        db.menus.delete_one({"_id": ObjectId(id)})
        flash(f"Menu '{menu_to_delete.get('name')}' supprimé avec succès", "success")
        
    except Exception as e:
        flash(f"Erreur lors de la suppression: {str(e)}", "error")
    
    return redirect(url_for("nutrition_bp.manage_menus"))
