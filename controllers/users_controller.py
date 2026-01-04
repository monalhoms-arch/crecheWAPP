from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from bson.objectid import ObjectId
from db import db
from models.user import User
from utils.decorators import admin_required

users_bp = Blueprint("users_bp", __name__, template_folder="../templates")

@users_bp.route("/", methods=["GET"])
@admin_required
def list_users():
    users = list(db.users.find().sort("username", 1))
    
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user['_id'] = str(user['_id'])
    
    # Create a mapping of ID -> Name for all potential related profiles
    related_map = {}
    
    # Fetch full lists for the Add User form
    all_parents = list(db.parents.find({}, {"_id": 1, "nom": 1}))
    all_educateurs = list(db.educateurs.find({}, {"_id": 1, "nom": 1}))
    all_dietitians = list(db.dietitians.find({}, {"_id": 1, "nom": 1}))

    for p in all_parents:
        related_map[str(p["_id"])] = p["nom"]
    for e in all_educateurs:
        related_map[str(e["_id"])] = e["nom"]
    for d in all_dietitians:
        related_map[str(d["_id"])] = d["nom"]
        
    return render_template("users/list.html", users=users, related_map=related_map, 
                           parents=all_parents, educateurs=all_educateurs, dietitians=all_dietitians)

@users_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        related_id = request.form.get("related_id") or None
        
        # Check if username exists
        if db.users.find_one({"username": username}):
            flash("Ce nom d'utilisateur existe déjà")
            return redirect(url_for("users_bp.add_user"))
            
        u = User(username=username, role=role, related_id=related_id)
        u.set_password(password)
        db.users.insert_one(u.to_dict())
        flash(f"Utilisateur {username} créé")
        return redirect(url_for("users_bp.list_users"))
        
    # Fetch potential related profiles (Parents, Educateurs, Dietitians)
    parents = list(db.parents.find())
    educateurs = list(db.educateurs.find())
    dietitians = list(db.dietitians.find())
    return render_template("users/add.html", parents=parents, educateurs=educateurs, dietitians=dietitians)

@users_bp.route("/delete/<id>", methods=["GET", "POST"])
@admin_required
def delete_user(id):
    try:
        user_to_delete = db.users.find_one({"_id": ObjectId(id)})
        if not user_to_delete:
            flash("Utilisateur introuvable", "error")
            return redirect(url_for("users_bp.list_users"))
        
        # Prevent deleting the hardcoded 'admin' user or self
        if user_to_delete['username'] == 'admin':
            flash("Impossible de supprimer l'administrateur principal", "error")
            return redirect(url_for("users_bp.list_users"))
            
        if user_to_delete['username'] == current_user.username:
             flash("Impossible de supprimer votre propre compte", "error")
             return redirect(url_for("users_bp.list_users"))

        db.users.delete_one({"_id": ObjectId(id)})
        flash(f"Utilisateur {user_to_delete['username']} supprimé avec succès", "success")
        
    except Exception as e:
        flash(f"Erreur lors de la suppression: {str(e)}", "error")
    
    # Force reload by adding cache-busting parameter
    from flask import make_response
    response = make_response(redirect(url_for("users_bp.list_users")))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@users_bp.route("/edit/<id>", methods=["POST"])
@admin_required
def edit_user(id):
    try:
        user_to_edit = db.users.find_one({"_id": ObjectId(id)})
        if not user_to_edit:
            flash("Utilisateur introuvable", "error")
            return redirect(url_for("users_bp.list_users"))
        
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        related_id = request.form.get("related_id") or None
        
        # Prevent changing admin username
        if user_to_edit['username'] == 'admin' and username != 'admin':
            flash("Impossible de modifier le nom de l'administrateur principal", "error")
            return redirect(url_for("users_bp.list_users"))
        
        # Check if new username already exists (if username changed)
        if username != user_to_edit['username']:
            if db.users.find_one({"username": username}):
                flash("Ce nom d'utilisateur existe déjà", "error")
                return redirect(url_for("users_bp.list_users"))
        
        # Prepare update data
        update_data = {
            "username": username,
            "role": role,
            "related_id": related_id
        }
        
        # Only update password if provided
        if password:
            u = User(username=username, role=role)
            u.set_password(password)
            update_data["password_hash"] = u.password_hash
        
        db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        flash(f"Utilisateur {username} modifié avec succès", "success")
        
    except Exception as e:
        flash(f"Erreur lors de la modification: {str(e)}", "error")
    
    return redirect(url_for("users_bp.list_users"))

