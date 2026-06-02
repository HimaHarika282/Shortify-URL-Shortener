from flask import Flask, render_template, session, redirect
from models import db
import config
import os

from routes.url_routes import url_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

# Load config
app.config.from_object(config)

# Secret key
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")

# IMPORTANT FOR RENDER HTTPS SESSIONS
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Initialize DB
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tables created successfully!")

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():

    if not session.get("user_id"):
        return redirect('/login')

    return render_template('dashboard.html')

@app.route('/check-session')
def check_session():

    if session.get("user_id"):
        return {"logged_in": True}

    return {"logged_in": False}

app.register_blueprint(url_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True)