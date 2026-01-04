from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from db import db

auth_bp = Blueprint('auth', __name__)

users_collection = db['users']

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users_collection.find_one({'username': username})
        
        if user_data:
            user_obj = User(
                username=user_data['username'],
                role=user_data['role'],
                password_hash=user_data['password_hash'],
                _id=str(user_data['_id']),
                related_id=user_data.get('related_id')
            )
            
            if user_obj.check_password(password):
                login_user(user_obj)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
        
        flash('Nom d\'utilisateur ou mot de passe incorrect')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/create_admin')
def create_admin():
    # Helper route to create initial admin - DELETE IN PRODUCTION
    if users_collection.find_one({'username': 'admin'}):
        return "Admin already exists"
    
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')
    users_collection.insert_one(admin.to_dict())
    return "Admin created: admin/admin123"
