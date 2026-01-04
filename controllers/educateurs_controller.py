from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from models.educateur import Educateur
from utils.decorators import admin_required

educateurs_bp = Blueprint("educateurs_bp", __name__, template_folder="../templates")

@educateurs_bp.route("/", methods=["GET"])
@admin_required
def list_educateurs():
    eds = list(db.educateurs.find().sort("_id", -1))
    return render_template("educateurs.html", educateurs=eds)

@educateurs_bp.route("/add", methods=["POST"])
@admin_required
def add_educateur():
    nom = request.form.get("nom")
    specialite = request.form.get("specialite","")
    if nom:
        ed = Educateur(nom=nom, specialite=specialite)
        db.educateurs.insert_one(ed.to_dict())
    return redirect(url_for("educateurs_bp.list_educateurs"))

@educateurs_bp.route("/delete/<id>")
@admin_required
def delete_educateur(id):
    db.educateurs.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("educateurs_bp.list_educateurs"))
