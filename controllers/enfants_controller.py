from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from models.enfant import Enfant

enfants_bp = Blueprint("enfants_bp", __name__, template_folder="../templates")

@enfants_bp.route("/", methods=["GET"])
def list_enfants():
    enfants = list(db.enfants.find().sort("_id", -1))
    parents = {str(p['_id']): p['nom'] for p in db.parents.find()}
    return render_template("enfants.html", enfants=enfants, parents=parents)

@enfants_bp.route("/add", methods=["GET","POST"])
def add_enfant():
    if request.method == "POST":
        nom = request.form.get("nom")
        age = int(request.form.get("age",0))
        parent_id = request.form.get("parent_id") or None
        e = Enfant(nom=nom, age=age, parent_id=parent_id)
        db.enfants.insert_one(e.to_dict())
        return redirect(url_for("enfants_bp.list_enfants"))
    parents = list(db.parents.find())
    return render_template("enfants_add.html", parents=parents)

@enfants_bp.route("/delete/<id>")
def delete_enfant(id):
    db.enfants.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("enfants_bp.list_enfants"))
