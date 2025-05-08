# routes/auth_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash
from services.auth_service import authenticate_user
from services.db_service import db

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_routes.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = authenticate_user(email, password)
    if user:
        session['user_id'] = user['email']
        session['role'] = user['role']
        return redirect(url_for('home'))
    return render_template('login.html', error="Invalid credentials")

@auth_routes.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_routes.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if db['user_login'].find_one({"email": email}):
        return render_template('register.html', error="Email already exists")

    role_doc = db['user_role'].find_one({"role": "user"})
    if not role_doc:
        return render_template('register.html', error="User role not found")

    db['user_login'].insert_one({
        "email": email,
        "password": generate_password_hash(password),
        "role": role_doc["role"]
    })

    return redirect(url_for('auth_routes.login_page'))

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_routes.login_page'))
