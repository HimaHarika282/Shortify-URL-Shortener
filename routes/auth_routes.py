from flask import Blueprint, request, jsonify, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password too short"}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "User already exists"}), 400

    hashed = generate_password_hash(password)

    user = User(email=email, password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id

    return jsonify({"message": "Login successful"})

    print("EMAIL:", email)
    print("PASSWORD:", password)

    user = User.query.filter_by(email=email).first()
    print("DB USER:", user)
    print("DB PASSWORD:", user.password if user else None)

@auth_bp.route('/logout')
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})