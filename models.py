from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

<<<<<<< HEAD

=======
>>>>>>> d059f08 (final deployment stable version)
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

<<<<<<< HEAD
=======
    # ✅ RELATIONSHIP MUST BE INSIDE USER
>>>>>>> d059f08 (final deployment stable version)
    urls = db.relationship(
        'URL',
        backref='user',
        lazy=True
    )


class URL(db.Model):

    __tablename__ = 'urls'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    original_url = db.Column(
        db.Text,
        nullable=False
    )

    short_code = db.Column(
<<<<<<< HEAD
        db.String(10),
=======
        db.String(50),
>>>>>>> d059f08 (final deployment stable version)
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    click_count = db.Column(
        db.Integer,
        default=0
    )

    expiry_date = db.Column(
        db.DateTime,
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )


class Click(db.Model):

    __tablename__ = 'clicks'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    url_id = db.Column(
        db.Integer,
        db.ForeignKey('urls.id')
    )

    clicked_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )