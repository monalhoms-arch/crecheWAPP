from flask import Blueprint, render_template, request, redirect, url_for, send_file
from bson.objectid import ObjectId
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from db import db
from models.paiement import Paiement

paiements_bp = Blueprint("paiements_bp", __name__, template_folder="../templates")

@paiements_bp.route("/", methods=["GET"])
def list_paiements():
    pays = list(db.paiements.find().sort("_id", -1))
    enfants = {str(e['_id']): e['nom'] for e in db.enfants.find()}
    return render_template("paiements.html", paiements=pays, enfants=enfants)

@paiements_bp.route("/add", methods=["GET","POST"])
def add_paiement():
    if request.method == "POST":
        enfant_id = request.form.get("enfant_id")
        montant = float(request.form.get("montant",0))
        pay = Paiement(enfant_id=enfant_id, montant=montant, date=datetime.now())
        db.paiements.insert_one(pay.to_dict())
        # simple redirect to list (PDF generation removed per request)
        return redirect(url_for("paiements_bp.list_paiements"))
    enfants = list(db.enfants.find())
    return render_template("paiements_add.html", enfants=enfants)
