from flask import Blueprint, request, jsonify, session
from models import db, User
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():

    try:

        data = request.get_json()

        email = data.get('email').strip().lower()
        password = data.get('password')

        if not email or not password:
            return jsonify({
                "error": "Email and password required"
            }), 400

        if "@" not in email:
            return jsonify({
                "error": "Invalid email"
            }), 400

        if len(password) < 6:
            return jsonify({
                "error": "Password too short"
            }), 400

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:
            return jsonify({
                "error": "User already exists"
            }), 400

        hashed = generate_password_hash(password)

        user = User(
            email=email,
            password=hashed
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "Signup successful"
        })

    except Exception as e:

        print("SIGNUP ERROR:", e)

        return jsonify({
            "error": "Internal Server Error"
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        email = data.get('email').strip().lower()
        password = data.get('password')

        user = User.query.filter_by(
            email=email
        ).first()

<<<<<<< HEAD
        if not user:
            return jsonify({
                "error": "Invalid credentials"
            }), 401

        if not check_password_hash(
            user.password,
            password
        ):
            return jsonify({
                "error": "Invalid credentials"
            }), 401

        session["user_id"] = user.id

        return jsonify({
            "message": "Login successful"
        })

    except Exception as e:

        print("LOGIN ERROR:", e)

        return jsonify({
            "error": "Internal Server Error"
        }), 500

=======
    session["user_id"] = user.id
    print("EMAIL:", email)
    print("PASSWORD:", password)

    print("DB PASSWORD:", user.password if user else None)
    return jsonify({"message": "Login successful"})

    
>>>>>>> d059f08 (final deployment stable version)

@auth_bp.route('/logout')
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out"
    })