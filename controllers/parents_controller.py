from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from models.parent import Parent

parents_bp = Blueprint("parents_bp", __name__, template_folder="../templates")

@parents_bp.route("/", methods=["GET"])
def list_parents():
    parents = list(db.parents.find().sort("_id", -1))
    return render_template("parents.html", parents=parents)

@parents_bp.route("/add", methods=["POST"])
def add_parent():
    nom = request.form.get("nom")
    email = request.form.get("email","")
    telephone = request.form.get("telephone","")
    if nom:
        p = Parent(nom=nom, telephone=telephone, email=email)
        db.parents.insert_one(p.to_dict())
    return redirect(url_for("parents_bp.list_parents"))

@parents_bp.route("/edit/<id>", methods=["GET","POST"])
def edit_parent(id):
    if request.method == "POST":
        db.parents.update_one({"_id": ObjectId(id)}, {"$set": {
            "nom": request.form.get("nom"),
            "email": request.form.get("email",""),
            "telephone": request.form.get("telephone","")
        }})
        return redirect(url_for("parents_bp.list_parents"))
    parent = db.parents.find_one({"_id": ObjectId(id)})
    return render_template("parents_edit.html", parent=parent)

@parents_bp.route("/delete/<id>")
def delete_parent(id):
    db.parents.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("parents_bp.list_parents"))
