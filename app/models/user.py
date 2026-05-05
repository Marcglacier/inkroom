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

    provider = db.Column(db.String(50), default="local")
    google_id = db.Column(db.String(255), unique=True, nullable=True, index=True)

    email_verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # PASSWORD RESET
    # =========================

    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    # =========================
    # PROFILE
    # =========================

    bio = db.Column(db.Text, default="")
    location = db.Column(db.String(100), nullable=True)
    is_private = db.Column(db.Boolean, default=False)

    profile_picture = db.Column(db.String(255), nullable=True)

    # =========================
    # PASSWORD HELPERS
    # =========================

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)