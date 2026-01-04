from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from datetime import datetime
from flask_login import current_user
from db import db
from models.presence import Presence
from utils.decorators import role_required

presence_bp = Blueprint("presence_bp", __name__, template_folder="../templates")

@presence_bp.route("/", methods=["GET"])
@role_required(['admin', 'educateur', 'parent'])
def list_presences():
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    query = {"date": date}
    
    if current_user.role == 'parent':
        if not current_user.related_id:
            # No linked profile
            return render_template("presences.html", presences=[], enfants={}, date=date)
        
        # Get parent's children IDs
        my_children = list(db.enfants.find({"parent_id": current_user.related_id}))
        child_ids = [str(c['_id']) for c in my_children]
        
        # Filter presences for these children
        query["enfant_id"] = {"$in": child_ids}
        
    pres = list(db.presences.find(query).sort("_id", -1))
    
    enfants = {str(e['_id']): e['nom'] for e in db.enfants.find()}
    return render_template("presences.html", presences=pres, enfants=enfants, date=date)

@presence_bp.route("/add", methods=["GET","POST"])
@role_required(['educateur'])
def add_presence():
    if request.method == "POST":
        enfant_id = request.form.get("enfant_id")
        statut = request.form.get("statut")
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
        
        # DEBUG LOGGING
        print(f"DEBUG: add_presence POST. enfant_id='{enfant_id}' (type={type(enfant_id)}), statut='{statut}'")
        
        # Validation: Check for None, empty string, or "None" string
        if not enfant_id or enfant_id == "None":
            flash("Veuillez sélectionner un enfant", "error")
            return redirect(url_for("presence_bp.list_presences", date=date))

        try:
            # Verify child exists (extra safety)
            if not ObjectId.is_valid(enfant_id):
                 flash(f"ID Enfant invalide: {enfant_id}", "error")
                 return redirect(url_for("presence_bp.list_presences", date=date))

            enfant = db.enfants.find_one({'_id': ObjectId(enfant_id)})
            if not enfant:
                flash("Enfant introuvable", "error")
                return redirect(url_for("presence_bp.list_presences", date=date))
                
            nom_enfant = enfant['nom']
            
            # Upsert: Update if exists, otherwise Insert
            db.presences.update_one(
                {"enfant_id": enfant_id, "date": date},
                {"$set": {"statut": statut, "nom_enfant": nom_enfant}},
                upsert=True
            )
            flash("Présence mise à jour", "success")
            
        except Exception as e:
            print(f"EXCEPTION in add_presence: {e}")
            flash(f"Erreur lors de l'enregistrement: {str(e)}", "error")
            
        return redirect(url_for("presence_bp.list_presences", date=date))
    
    # Get method should just redirect back to list
    return redirect(url_for("presence_bp.list_presences"))
