# app/models/user.py
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=True)

    provider = db.Column(db.String(50), default="local")  # local | google

    google_id = db.Column(db.String(255), unique=True, nullable=True, index=True)

    email_verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy=True, cascade="all, delete-orphan")
    messages = db.relationship("Message", backref="sender", lazy=True, cascade="all, delete-orphan")

    # password handling
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)

    # oauth helper
    def set_google_user(self, google_id):
        self.provider = "google"
        self.google_id = google_id
        self.email_verified = True