from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from datetime import datetime, date as date_obj
from flask_login import current_user
from db import db
from models.presence import Presence
from utils.decorators import role_required

presence_bp = Blueprint("presence_bp", __name__, template_folder="../templates")

@presence_bp.route("/", methods=["GET"])
@role_required(['admin', 'educateur', 'parent'])
def list_presences():
    # Default to today
    selected_date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    edit_id = request.args.get("edit_id")
    
    # Future Date Validation (Backend)
    if selected_date_str > datetime.now().strftime("%Y-%m-%d"):
        flash("Impossible de consulter ou modifier des présences futures.", "warning")
        return redirect(url_for("presence_bp.list_presences")) # Defaults to today

    # 1. Fetch Children based on Role
    children_query = {}
    if current_user.role == 'parent':
        if not current_user.related_id:
             return render_template("presences.html", register=[], stats={}, date=selected_date_str)
        children_query["parent_id"] = current_user.related_id
    elif current_user.role == 'educateur':
        # Optionally filter by educateur's group if strictly enforced
        pass 

    all_children = list(db.enfants.find(children_query))
    
    # 2. Fetch Presences for selected date
    presence_query = {"date": selected_date_str}
    if current_user.role == 'parent':
         # Parents only see their kids' presences
         child_ids = [str(c['_id']) for c in all_children]
         presence_query["enfant_id"] = {"$in": child_ids}
         
    presences_list = list(db.presences.find(presence_query))
    
    # Check for edit context
    presence_to_edit = None
    if edit_id:
        # Find the specific presence
        # We search in the list first to avoid extra DB call, or just DB call?
        # DB call is safer
        presence_to_edit = db.presences.find_one({"_id": ObjectId(edit_id)})
        if presence_to_edit:
             presence_to_edit['_id'] = str(presence_to_edit['_id'])
    
    # 3. Merge Data (Register View)
    presence_map = {p['enfant_id']: p for p in presences_list}
    
    register = []
    stats = {"present": 0, "absent": 0, "retard": 0, "total": len(all_children)}
    
    for child in all_children:
        child_id = str(child['_id'])
        p = presence_map.get(child_id)
        
        # Prepare row data
        row = {
            "child": child,
            "presence": p, # Can be None
            "status": p['statut'] if p else 'non_defini'
        }
        
        # Update Stats
        if p:
            if p['statut'] in stats:
                stats[p['statut']] += 1
                
        register.append(row)
        
    return render_template("presences.html", 
                         register=register, 
                         stats=stats, 
                         date=selected_date_str,
                         today=datetime.now().strftime("%Y-%m-%d"),
                         presence_to_edit=presence_to_edit)

@presence_bp.route("/add", methods=["POST"])
@role_required(['educateur', 'admin'])
def add_presence():
    enfant_id = request.form.get("enfant_id")
    statut = request.form.get("statut")
    selected_date = request.form.get("date")
    heure_arrivee = request.form.get("heure_arrivee")
    heure_depart = request.form.get("heure_depart")

    # validation
    if selected_date > datetime.now().strftime("%Y-%m-%d"):
        flash("Erreur: Date future interdite.", "error")
        return redirect(url_for("presence_bp.list_presences"))

    if not enfant_id:
        flash("Enfant requis", "error")
        return redirect(url_for("presence_bp.list_presences", date=selected_date))

    # Fetch child name
    child = db.enfants.find_one({"_id": ObjectId(enfant_id)})
    if not child:
        flash("Enfant introuvable", "error")
        return redirect(url_for("presence_bp.list_presences", date=selected_date))
        
    update_data = {
        "statut": statut,
        "nom_enfant": child['nom'],
        "heure_arrivee": heure_arrivee,
        "heure_depart": heure_depart
    }

    db.presences.update_one(
        {"enfant_id": enfant_id, "date": selected_date},
        {"$set": update_data},
        upsert=True
    )
    
    flash("Présence enregistrée", "success")
    return redirect(url_for("presence_bp.list_presences", date=selected_date))
    
@presence_bp.route("/edit/<id>", methods=["GET", "POST"])
@role_required(['educateur', 'admin'])
def edit_presence(id):
    # This route might be less used now if we use the main register view, 
    # but keeping it for the Edit button on the row.
    p = db.presences.find_one({"_id": ObjectId(id)})
    if not p:
        flash("Introuvable", "error")
        return redirect(url_for("presence_bp.list_presences"))
        
    if request.method == "POST":
        statut = request.form.get("statut")
        heure_arrivee = request.form.get("heure_arrivee")
        heure_depart = request.form.get("heure_depart")
        
        db.presences.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "statut": statut,
                "heure_arrivee": heure_arrivee,
                "heure_depart": heure_depart
            }}
        )
        flash("Mis à jour", "success")
        return redirect(url_for("presence_bp.list_presences", date=p['date']))

    # To render the edit VIEW properly with the new merged logic, 
    # we need to redirect to list_presence with a special flag or just use the modal logic?
    # Actually, the previous implementation rendered the list with `presence_to_edit`.
    # Let's adapt list_presences to handle this context if passed?
    # Or cleaner: Since I'm doing a Register View, maybe the "Edit" is just 
    # re-opening the "Add" form (which is an Upsert) but pre-filled?
    # BUT, `edit_presence` logic is slightly different (takes ID).
    # Let's keep it simple: Re-use list_presences logic but pass `presence_to_edit`.
    
    # Call list_presences logic manually (refactoring into a helper would be best, but copy-paste for now is safer for tool reliance)
    # Actually, let's just Redirect to list and pass 'edit_id' param?
    # No, that requires template logic.
    
    # Let's fetch the data needed for list_presences
    selected_date_str = p['date']
    
    # ... (Same fetch logic as list_presences) ...
    # RE-IMPLEMENTATION of list_presences logic here is risky for code duplication.
    # BETTER: Render `presences.html` with the minimal needed + presence_to_edit
    # But presences.html EXPECTS `register` list.
    
    # Let's Redirect to main list with `edit_id` as query param?
    # And handle `edit_id` in `list_presences`.
    return redirect(url_for("presence_bp.list_presences", date=selected_date_str, edit_id=id))
