from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from models.dietitian import Dietitian
from utils.decorators import admin_required

dietitians_bp = Blueprint("dietitians_bp", __name__, template_folder="../templates")

@dietitians_bp.route("/", methods=["GET"])
@admin_required
def list_dietitians():
    diets = list(db.dietitians.find().sort("_id", -1))
    return render_template("dietitians.html", dietitians=diets)

@dietitians_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_dietitian():
    if request.method == "POST":
        nom = request.form.get("nom")
        telephone = request.form.get("telephone")
        email = request.form.get("email")
        specialite = request.form.get("specialite")
        
        d = Dietitian(nom=nom, telephone=telephone, email=email, specialite=specialite)
        db.dietitians.insert_one(d.to_dict())
        return redirect(url_for("dietitians_bp.list_dietitians"))
    return render_template("dietitians_add.html")

@dietitians_bp.route("/delete/<id>")
@admin_required
def delete_dietitian(id):
    db.dietitians.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("dietitians_bp.list_dietitians"))

@dietitians_bp.route("/edit/<id>", methods=["GET", "POST"])
@admin_required
def edit_dietitian(id):
    dietitian = db.dietitians.find_one({"_id": ObjectId(id)})
    if not dietitian:
        return redirect(url_for("dietitians_bp.list_dietitians"))
        
    if request.method == "POST":
        nom = request.form.get("nom")
        telephone = request.form.get("telephone")
        email = request.form.get("email")
        specialite = request.form.get("specialite")
        
        db.dietitians.update_one({"_id": ObjectId(id)}, {"$set": {
            "nom": nom,
            "telephone": telephone,
            "email": email,
            "specialite": specialite
        }})
        return redirect(url_for("dietitians_bp.list_dietitians"))
    
    # For GET, we render the SAME main page, but with the data to edit
    diets = list(db.dietitians.find().sort("_id", -1))
    return render_template("dietitians.html", dietitians=diets, dietitian_to_edit=dietitian)
