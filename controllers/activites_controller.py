from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from flask_login import login_required
from db import db
from models.activite import Activite
from utils.decorators import admin_required, role_required

activites_bp = Blueprint("activites_bp", __name__, template_folder="../templates")

@activites_bp.route("/", methods=["GET"])
@login_required # All authenticated users can see activities
def list_activites():
    acts = list(db.activites.find().sort("date", 1))
    for a in acts:
        a['_id'] = str(a['_id'])
    return render_template("activites.html", activites=acts)

@activites_bp.route("/add", methods=["POST"])
@role_required(['educateur', 'admin'])
def add_activite():
    titre = request.form.get("titre")
    description = request.form.get("description","")
    date = request.form.get("date","")
    if titre:
        a = Activite(titre=titre, description=description, date=date)
        db.activites.insert_one(a.to_dict())
        flash("Activité ajoutée avec succès", "success")
    return redirect(url_for("activites_bp.list_activites"))

@activites_bp.route("/edit/<id>", methods=["GET", "POST"])
@role_required(['educateur', 'admin'])
def edit_activite(id):
    act = db.activites.find_one({"_id": ObjectId(id)})
    if not act:
        flash("Activité introuvable", "error")
        return redirect(url_for("activites_bp.list_activites"))

    if request.method == "POST":
        titre = request.form.get("titre")
        description = request.form.get("description","")
        date = request.form.get("date","")
        
        if titre:
            db.activites.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "titre": titre,
                    "description": description,
                    "date": date
                }}
            )
            flash("Activité modifiée avec succès", "success")
        return redirect(url_for("activites_bp.list_activites"))
    
    # GET: Render list with edit context
    acts = list(db.activites.find().sort("date", 1))
    for a in acts:
        a['_id'] = str(a['_id'])
        
    return render_template("activites.html", activites=acts, activite_to_edit=act)

@activites_bp.route("/delete/<id>")
@role_required(['admin', 'educateur'])
def delete_activite(id):
    db.activites.delete_one({"_id": ObjectId(id)})
    flash("Activité supprimée", "info")
    return redirect(url_for("activites_bp.list_activites"))
