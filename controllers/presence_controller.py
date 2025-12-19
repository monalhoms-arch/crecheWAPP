from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from datetime import datetime
from db import db
from models.presence import Presence

presence_bp = Blueprint("presence_bp", __name__, template_folder="../templates")

@presence_bp.route("/", methods=["GET"])
def list_presences():
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    pres = list(db.presences.find({"date": date}).sort("_id", -1))
    enfants = {str(e['_id']): e['nom'] for e in db.enfants.find()}
    return render_template("presences.html", presences=pres, enfants=enfants, date=date)

@presence_bp.route("/add", methods=["GET","POST"])
def add_presence():
    if request.method == "POST":
        enfant_id = request.form.get("enfant_id")
        statut = request.form.get("statut")
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
        nom_enfant = db.enfants.find_one({'_id': ObjectId(enfant_id)})['nom']
        p = Presence(enfant_id=enfant_id, nom_enfant=nom_enfant, date=date, statut=statut)
        db.presences.insert_one(p.to_dict())
        return redirect(url_for("presence_bp.list_presences"))
    enfants = list(db.enfants.find())
    return render_template("presences_add.html", enfants=enfants)
