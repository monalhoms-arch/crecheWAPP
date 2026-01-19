from flask import Flask, redirect, url_for, render_template
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Controllers need to be imported AFTER app init generally if circular logic exists,
# but here specific blueprints are imported from controllers.

from flask_login import LoginManager, login_required, current_user
from controllers.auth_controller import auth_bp
from models.user import User    
from db import db

# Initialize Flask app FIRST
app = Flask(__name__)
app.secret_key = "change_this_secret"

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

@login_manager.user_loader
def load_user(username):
    user_data = db['users'].find_one({'username': username})
    if not user_data:
        return None
    return User(
        username=user_data['username'],
        role=user_data['role'],
        password_hash=user_data['password_hash'],
        _id=str(user_data['_id']),
        related_id=user_data.get('related_id')
    )

# Import Blueprints
from controllers.parents_controller import parents_bp
from controllers.enfants_controller import enfants_bp
from controllers.educateurs_controller import educateurs_bp
from controllers.activites_controller import activites_bp
from controllers.presence_controller import presence_bp
from controllers.paiements_controller import paiements_bp
from controllers.groups_controller import groups_bp
from controllers.nutrition_controller import nutrition_bp
from controllers.communication_controller import communication_bp
from controllers.users_controller import users_bp
from controllers.dietitians_controller import dietitians_bp

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(parents_bp, url_prefix='/parents')
app.register_blueprint(enfants_bp, url_prefix='/enfants')
app.register_blueprint(educateurs_bp, url_prefix='/educateurs')
app.register_blueprint(groups_bp, url_prefix='/groups')
app.register_blueprint(nutrition_bp, url_prefix='/nutrition')
app.register_blueprint(communication_bp, url_prefix='/communication')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(dietitians_bp, url_prefix='/dietitians')
app.register_blueprint(activites_bp, url_prefix="/activites")
app.register_blueprint(presence_bp, url_prefix="/presences")
app.register_blueprint(paiements_bp, url_prefix="/paiements")

@app.route("/")
@login_required 
def index():
    stats = {
        'today_date': datetime.now().strftime("%d/%m/%Y"),
        'pending_payments': 0,
        'unread_messages': 0,
        'enfants_count': 0,
        'parents_count': 0,
        'educateurs_count': 0,
        'dietitians_count': 0,
        'users_count': 0,
        'recent_payments': [],
        'my_children': [],
        'my_groups': [],
        'allergy_kids_count': 0,
        'meals_count': 0
    }
    
    # ADMIN DASHBOARD STATS
    if current_user.role == 'admin':
        stats['parents_count'] = db.parents.count_documents({})
        stats['enfants_count'] = db.enfants.count_documents({})
        stats['educateurs_count'] = db.educateurs.count_documents({})
        stats['users_count'] = db.users.count_documents({})
        stats['dietitians_count'] = db.dietitians.count_documents({})
        # Recent payments
        stats['recent_payments'] = list(db.paiements.find().sort("date", -1).limit(5))
    
    # EDUCATEUR DASHBOARD STATS
    elif current_user.role == 'educateur':
        if current_user.related_id:
            # My Groups
            # Handle both String and ObjectId for robustness
            rid = current_user.related_id
            possible_ids = [rid]
            try:
                from bson.objectid import ObjectId
                possible_ids.append(ObjectId(rid))
            except:
                pass
            
            my_groups = list(db.groups.find({"educateur_id": {"$in": possible_ids}}))
            stats['my_groups'] = my_groups
            # Children count in my groups (approximate or need agg)
            # For simplicity, just show groups count or fetch children if needed
            stats['groups_count'] = len(my_groups)
            
            # Today's activities
            today = datetime.now().strftime("%Y-%m-%d")
            # stats['activities_today'] = list(db.activites.find({"date": today, "educateur_id": current_user.related_id})) 
            # (Activites model date format might vary, assuming string YYYY-MM-DD)

    # PARENT DASHBOARD STATS
    elif current_user.role == 'parent':
        if current_user.related_id:
            # My Children
            my_children = list(db.enfants.find({"parent_id": current_user.related_id}))
            stats['my_children'] = my_children
            stats['children_count'] = len(my_children)
            
            # Pending Payments
            child_ids = [str(c['_id']) for c in my_children]
            pending_count = db.paiements.count_documents({"enfant_id": {"$in": child_ids}, "statut": "en_attente"})
            stats['pending_payments'] = pending_count
            
            # Unread Messages (Stub - assume 0 for now or implement if message model ready)
            stats['unread_messages'] = 0

    # DIETITIAN DASHBOARD STATS
    elif current_user.role == 'dietitian':
        # Today's meals count
        today = datetime.now().strftime("%Y-%m-%d")
        stats['meals_count'] = db.meals.count_documents({"date": today})
        # Children with allergies count
        stats['allergy_kids_count'] = db.enfants.count_documents({"allergies": {"$ne": []}})

    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    # Disable the automatic reloader when running under the VS Code debugger.
    # The reloader tries to re-import the module by name which conflicts
    # with the local `app` package directory and raises SystemExit(1).
    app.run(debug=True, use_reloader=False)