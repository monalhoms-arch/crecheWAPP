from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from models.group import Group
from flask_login import current_user
from utils.decorators import admin_required, role_required

groups_bp = Blueprint("groups_bp", __name__, template_folder="../templates")

@groups_bp.route("/", methods=["GET"])
@role_required(['admin', 'educateur'])
def list_groups():
    groups = list(db.groups.find().sort("_id", -1))
    # Dictionary for table lookup (ID -> Name)
    educateurs_map = {str(e['_id']): e['nom'] for e in db.educateurs.find()}
    # List for dropdown
    educateurs_list = list(db.educateurs.find())
    
    return render_template("groups.html", groups=groups, educateurs=educateurs_map, educateurs_list=educateurs_list)

@groups_bp.route("/add", methods=["POST"])
@admin_required
def add_group():
    nom = request.form.get("nom")
    capacity = int(request.form.get("capacity", 0))
    age_range = request.form.get("age_range")
    educateur_id = request.form.get("educateur_id") or None
    
    if nom:
        g = Group(nom=nom, capacity=capacity, age_range=age_range, educateur_id=educateur_id)
        db.groups.insert_one(g.to_dict())
    return redirect(url_for("groups_bp.list_groups"))

@groups_bp.route("/delete/<id>")
@admin_required
def delete_group(id):
    db.groups.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("groups_bp.list_groups"))
