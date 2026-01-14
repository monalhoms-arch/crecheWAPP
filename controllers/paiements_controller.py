from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from bson.objectid import ObjectId
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from flask_login import login_required, current_user
from db import db
from models.paiement import Paiement
from utils.decorators import admin_required
import os
import requests

paiements_bp = Blueprint("paiements_bp", __name__, template_folder="../templates")

@paiements_bp.route("/", methods=["GET"])
@login_required
def list_paiements():
    query = {}
    invoice_query = {}
    
    if current_user.role == 'parent':
        if current_user.related_id:
            # Find children for this parent
            parent_children = list(db.enfants.find({"parent_id": current_user.related_id}))
            children_ids = [str(c['_id']) for c in parent_children]
            query = {"enfant_id": {"$in": children_ids}}
            # Filter invoices for parents as well
            child_names = [c['nom'] for c in parent_children]
            invoice_query = {"child_name": {"$in": child_names}}
        else:
            # No linked parent profile? Show nothing.
            query = {"enfant_id": "none"}
            invoice_query = {"child_name": "none"}
             
    pays = list(db.paiements.find(query).sort("_id", -1))
    invoices = list(db.invoices.find(invoice_query).sort("date", -1))
    
    # Calculate summary for parents
    total_pending = 0
    if current_user.role == 'parent':
        total_pending = sum(p.get('montant', 0) for p in pays if p.get('statut') == 'en_attente')

    # Helper for template: map enfant_id string to name
    enfants_map = {str(e['_id']): e['nom'] for e in db.enfants.find()}
    all_enfants = list(db.enfants.find({}, {"_id": 1, "nom": 1}))
    
    # Ensure IDs are stringified for consistent template usage
    for e in all_enfants:
        e['_id'] = str(e['_id'])
    for p in pays:
        p['_id'] = str(p['_id'])
        # Ensure date is formatted if it's a datetime object
        if isinstance(p.get('date'), datetime):
            p['date_str'] = p['date'].strftime('%d/%m/%Y')
        else:
            p['date_str'] = str(p.get('date'))
        
    return render_template("paiements.html", 
                         paiements=pays, 
                         invoices=invoices, 
                         enfants=enfants_map, 
                         all_enfants=all_enfants,
                         total_pending=total_pending)

from models.invoice import Invoice
import uuid

@paiements_bp.route("/add", methods=["POST"])
@admin_required
def add_paiement():
    enfant_id = request.form.get("enfant_id")
    montant = float(request.form.get("montant", 0))
    statut = request.form.get("statut", "paye")
    
    # Create Payment
    pay = Paiement(enfant_id=enfant_id, montant=montant, date=datetime.now(), statut=statut)
    db.paiements.insert_one(pay.to_dict())
    
    # Create Invoice automatically
    enfant = db.enfants.find_one({"_id": ObjectId(enfant_id)})
    parent_name = "Inconnu"
    if enfant and enfant.get('parent_id'):
        parent = db.parents.find_one({"_id": ObjectId(enfant['parent_id'])})
        if parent: 
            parent_name = parent['nom']
        
    inv = Invoice(
        invoice_number=str(uuid.uuid4())[:8].upper(),
        amount=montant,
        child_name=enfant['nom'] if enfant else "N/A",
        parent_name=parent_name
    )
    db.invoices.insert_one(inv.to_dict())
    
    flash("Paiement enregistré et facture générée", "success")
    return redirect(url_for("paiements_bp.list_paiements"))

@paiements_bp.route("/invoice/<invoice_number>")
@login_required
def download_invoice(invoice_number):
    inv_data = db.invoices.find_one({"invoice_number": invoice_number})
    if not inv_data:
        flash("Facture introuvable", "error")
        return redirect(url_for("paiements_bp.list_paiements"))
    
    # Security: Parents should only download their own children's invoices
    if current_user.role == 'parent':
        if not current_user.related_id:
            return "Unauthorized", 403
        
        parent_children = list(db.enfants.find({"parent_id": current_user.related_id}, {"nom": 1}))
        child_names = [c['nom'] for c in parent_children]
        
        if inv_data.get('child_name') not in child_names:
            flash("Accès non autorisé à cette facture", "error")
            return redirect(url_for("paiements_bp.list_paiements"))

    inv = Invoice(**{k:v for k,v in inv_data.items() if k != '_id'})
    pdf = inv.generate_pdf()
    
    return send_file(pdf, as_attachment=True, download_name=f"facture_{invoice_number}.pdf", mimetype='application/pdf')

@paiements_bp.route("/pay/<id>")
@login_required
def pay_now(id):
    if current_user.role != 'parent':
        flash("Action non autorisée", "error")
        return redirect(url_for("paiements_bp.list_paiements"))

    paiement = db.paiements.find_one({"_id": ObjectId(id)})
    if not paiement:
        flash("Paiement introuvable", "error")
        return redirect(url_for("paiements_bp.list_paiements"))

    # Chargily API configuration
    chargily_api_key = os.getenv('CHARGILY_API_KEY')
    chargily_secret_key = os.getenv('CHARGILY_SECRET_KEY')
    chargily_url = 'https://pay.chargily.net/test/api/v2/checkouts'  # Test mode (use .net)

    # Create checkout session
    checkout_data = {
        'amount': paiement['montant'],
        'currency': 'dzd',  # Algerian Dinar
        'success_url': url_for('paiements_bp.payment_success', id=id, _external=True),
        'failure_url': url_for('paiements_bp.payment_failure', id=id, _external=True),
        # webhook_url is removed because Chargily rejects localhost/127.0.0.1
        'description': f'Paiement pour {paiement["enfant_id"]}',
        'metadata': {'paiement_id': str(id)}
    }

    headers = {
        'Authorization': f'Bearer {chargily_secret_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(chargily_url, json=checkout_data, headers=headers)
        response.raise_for_status()
        checkout = response.json()

        # Store chargily_payment_id
        db.paiements.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"chargily_payment_id": checkout['id']}}
        )
        # Redirect to Chargily checkout URL
        return redirect(checkout['checkout_url'])
    except requests.exceptions.HTTPError as e:
        error_msg = response.text if 'response' in locals() else str(e)
        flash(f"Erreur lors de la création du paiement (Chargily): {error_msg}", "error")
        return redirect(url_for("paiements_bp.list_paiements"))
    except requests.exceptions.RequestException as e:
        flash(f"Erreur de connexion lors de la création du paiement: {str(e)}", "error")
        return redirect(url_for("paiements_bp.list_paiements"))

@paiements_bp.route("/payment/success/<id>")
@login_required
def payment_success(id):
    # Update payment status to paid
    db.paiements.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"statut": "paye", "date": datetime.now(), "mode": "chargily"}}
    )
    flash("Paiement effectué avec succès via Chargily", "success")
    return redirect(url_for("paiements_bp.list_paiements"))

@paiements_bp.route("/pay_manual/<id>")
@login_required
def pay_manual(id):
    if current_user.role != 'parent':
        flash("Action non autorisée", "error")
        return redirect(url_for("paiements_bp.list_paiements"))

    paiement = db.paiements.find_one({"_id": ObjectId(id)})
    if not paiement:
        flash("Paiement introuvable", "error")
        return redirect(url_for("paiements_bp.list_paiements"))

    # Update payment mode to espèce but keep status as pending
    db.paiements.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"mode": "espece", "statut": "en_attente"}}
    )
    
    flash("Demande de paiement en espèces enregistrée. Veuillez vous présenter à l'administration pour finaliser le paiement.", "info")
    return redirect(url_for("paiements_bp.list_paiements"))

@paiements_bp.route("/payment/failure/<id>")
@login_required
def payment_failure(id):
    flash("Paiement annulé ou échoué", "error")
    return redirect(url_for("paiements_bp.list_paiements"))

@paiements_bp.route("/payment/webhook/<id>", methods=["POST"])
def payment_webhook(id):
    # Handle webhook from Chargily
    data = request.json
    if data.get('status') == 'paid':
        db.paiements.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"statut": "paye", "date": datetime.now(), "mode": "chargily"}}
        )
    return '', 200

@paiements_bp.route("/edit/<id>", methods=["GET", "POST"])
@admin_required
def edit_paiement(id):
    paiement = db.paiements.find_one({"_id": ObjectId(id)})
    if not paiement:
        flash("Paiement introuvable", "error")
        return redirect(url_for("paiements_bp.list_paiements"))

    if request.method == "POST":
        try:
            update_data = {
                "enfant_id": request.form.get("enfant_id"),
                "montant": float(request.form.get("montant", 0)),
                "statut": request.form.get("statut")
            }
            db.paiements.update_one({"_id": ObjectId(id)}, {"$set": update_data})
            flash("Paiement mis à jour avec succès", "success")
        except Exception as e:
            flash(f"Erreur lors de la modification: {str(e)}", "error")
        return redirect(url_for("paiements_bp.list_paiements"))
    
    # GET: Render list with edit context
    # Admin only, so we show all payments usually, or same query as list_paiements
    pays = list(db.paiements.find({}).sort("_id", -1))
    invoices = list(db.invoices.find({}).sort("date", -1))
    
    enfants_map = {str(e['_id']): e['nom'] for e in db.enfants.find()}
    all_enfants = list(db.enfants.find({}, {"_id": 1, "nom": 1}))
    
    # Process data for template (str IDs, dates)
    for e in all_enfants:
        e['_id'] = str(e['_id'])
    for p in pays:
        p['_id'] = str(p['_id'])
        if isinstance(p.get('date'), datetime):
            p['date_str'] = p['date'].strftime('%d/%m/%Y')
        else:
            p['date_str'] = str(p.get('date'))
            
    return render_template("paiements.html", 
                         paiements=pays, 
                         invoices=invoices, 
                         enfants=enfants_map, 
                         all_enfants=all_enfants,
                         total_pending=0, # Admin doesn't need total pending usually
                         paiement_to_edit=paiement)

@paiements_bp.route("/delete/<id>")
@admin_required
def delete_paiement(id):
    db.paiements.delete_one({"_id": ObjectId(id)})
    flash("Paiement supprimé avec succès", "success")
    return redirect(url_for("paiements_bp.list_paiements"))
