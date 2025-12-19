from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from models.activite import Activite

activites_bp = Blueprint("activites_bp", __name__, template_folder="../templates")

@activites_bp.route("/", methods=["GET"])
def list_activites():
    acts = list(db.activites.find().sort("date", 1))
    return render_template("activites.html", activites=acts)

@activites_bp.route("/add", methods=["POST"])
def add_activite():
    titre = request.form.get("titre")
    description = request.form.get("description","")
    date = request.form.get("date","")
    if titre:
        a = Activite(titre=titre, description=description, date=date)
        db.activites.insert_one(a.to_dict())
    return redirect(url_for("activites_bp.list_activites"))

@activites_bp.route("/delete/<id>")
def delete_activite(id):
    db.activites.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("activites_bp.list_activites"))
