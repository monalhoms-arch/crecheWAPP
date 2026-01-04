from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from flask_login import current_user, login_required
from db import db
from models.communication import Message, Complaint
from models.user import User

communication_bp = Blueprint("communication_bp", __name__, template_folder="../templates")

@communication_bp.route("/inbox", methods=["GET"])
@login_required
def inbox():
    messages = list(db.messages.find({"recipient_id": current_user.username}).sort("timestamp", -1))
    return render_template("communication/inbox.html", messages=messages)

@communication_bp.route("/send", methods=["GET", "POST"])
@login_required
def send_message():
    if request.method == "POST":
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")
        
        # Verify recipient exists
        if not db.users.find_one({"username": recipient}):
            flash("Destinataire introuvable")
            return redirect(url_for("communication_bp.send_message"))
            
        msg = Message(sender_id=current_user.username, recipient_id=recipient, subject=subject, body=body)
        db.messages.insert_one(msg.to_dict())
        flash("Message envoyé")
        return redirect(url_for("communication_bp.inbox"))
        
    users = list(db.users.find({}, {"username": 1, "role": 1}))
    return render_template("communication/send.html", users=users)

@communication_bp.route("/complaints", methods=["GET", "POST"])
@login_required
def complaints():
    # Parents: See own complaints, Create new
    # Admin: See all, Respond
    
    if request.method == "POST":
        if current_user.role != 'parent':
             return "Seuls les parents peuvent créer une plainte", 403
             
        title = request.form.get("title")
        desc = request.form.get("description")
        
        c = Complaint(parent_id=current_user.username, title=title, description=desc)
        db.complaints.insert_one(c.to_dict())
        return redirect(url_for("communication_bp.complaints"))
        
    query = {}
    if current_user.role == 'parent':
        query = {"parent_id": current_user.username}
        
    complaints_list = list(db.complaints.find(query).sort("timestamp", -1))
    return render_template("communication/complaints.html", complaints=complaints_list)

@communication_bp.route("/complaints/resolve/<id>", methods=["POST"])
@login_required
def resolve_complaint(id):
    if current_user.role != 'admin':
        return "Unauthorized", 403
        
    response = request.form.get("response")
    status = request.form.get("status")
    
    db.complaints.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"response": response, "status": status}}
    )
    return redirect(url_for("communication_bp.complaints"))
