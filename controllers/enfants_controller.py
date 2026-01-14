from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from flask_login import current_user
from db import db
from models.enfant import Enfant
from utils.decorators import admin_required, role_required

enfants_bp = Blueprint("enfants_bp", __name__, template_folder="../templates")

@enfants_bp.route("/", methods=["GET"])
@role_required(['admin', 'educateur', 'parent', 'dietitian'])
def list_enfants():
    # Check for allergy filter
    show_allergies_only = request.args.get('allergies') == 'true'
    
    if current_user.role == 'parent':
        if not current_user.related_id:
             return render_template("enfants.html", enfants=[], parents={})
        # Filter for children linked to this parent
        # Note: parent_id in Enfant might be string or ObjectId. Check for both if unsure, or enforce string.
        # Based on add_enfant, it saves as string.
        query = {"parent_id": current_user.related_id}
        if show_allergies_only:
            query["allergies"] = {"$exists": True, "$ne": []}
        enfants = list(db.enfants.find(query).sort("_id", -1))
    else:
        query = {}
        if show_allergies_only:
            query["allergies"] = {"$exists": True, "$ne": []}
        enfants = list(db.enfants.find(query).sort("_id", -1))
        
    parents_map = {str(p['_id']): p['nom'] for p in db.parents.find()}
    
    # For the add form (Admin only mostly, but fetching doesn't hurt)
    all_parents = list(db.parents.find())
    all_groups = list(db.groups.find())
    
    return render_template("enfants.html", enfants=enfants, parents=parents_map, all_parents=all_parents, all_groups=all_groups, show_allergies_only=show_allergies_only)

@enfants_bp.route("/add", methods=["GET","POST"])
@admin_required
def add_enfant():
    if request.method == "POST":
        nom = request.form.get("nom")
        age = int(request.form.get("age",0))
        code = request.form.get("code", "")
        gender = request.form.get("gender", "")
        allergies_str = request.form.get("allergies", "")
        allergies = [a.strip() for a in allergies_str.split(',') if a.strip()]
        group_id = request.form.get("group_id") or None
        parent_id = request.form.get("parent_id") or None
        
        e = Enfant(
            nom=nom, 
            age=age, 
            code=code, 
            gender=gender, 
            allergies=allergies, 
            group_id=group_id, 
            parent_id=parent_id
        )
        db.enfants.insert_one(e.to_dict())
        return redirect(url_for("enfants_bp.list_enfants"))
    return redirect(url_for("enfants_bp.list_enfants"))

@enfants_bp.route("/edit/<id>", methods=["GET","POST"])
@admin_required
def edit_enfant(id):
    enfant = db.enfants.find_one({"_id": ObjectId(id)})
    if not enfant:
        return redirect(url_for("enfants_bp.list_enfants"))
        
    if request.method == "POST":
        allergies_str = request.form.get("allergies", "")
        allergies = [a.strip() for a in allergies_str.split(',') if a.strip()]
        
        update_data = {
            "nom": request.form.get("nom"),
            "age": int(request.form.get("age", 0)),
            "gender": request.form.get("gender"),
            "parent_id": request.form.get("parent_id") or None,
            "group_id": request.form.get("group_id") or None,
            "allergies": allergies
        }
        db.enfants.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return redirect(url_for("enfants_bp.list_enfants"))

    # Context for rendering the list view with edit form
    query = {}
    if request.args.get('allergies') == 'true':
        query["allergies"] = {"$exists": True, "$ne": []}
    
    enfants = list(db.enfants.find(query).sort("_id", -1))
    parents_map = {str(p['_id']): p['nom'] for p in db.parents.find()}
    all_parents = list(db.parents.find())
    all_groups = list(db.groups.find())
    
    return render_template("enfants.html", 
                         enfants=enfants, 
                         parents=parents_map, 
                         all_parents=all_parents, 
                         all_groups=all_groups, 
                         enfant_to_edit=enfant,
                         show_allergies_only=request.args.get('allergies') == 'true')

@enfants_bp.route("/delete/<id>")
@admin_required
def delete_enfant(id):
    db.enfants.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("enfants_bp.list_enfants"))
