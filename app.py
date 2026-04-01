from flask import Flask
from models import db, URL, User  
import config
from routes.url_routes import url_bp
from flask import render_template
from routes.auth_routes import auth_bp
import os

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")
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

from flask import session, redirect

@app.route('/dashboard')
def dashboard():
    if not session.get("user_id"):
        return redirect('/login')
    return render_template('dashboard.html')

app.register_blueprint(url_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)