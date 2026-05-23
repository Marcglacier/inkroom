# app/models/user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    # ================= CORE =================
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120))  # 👑 True Name
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text)
    provider = db.Column(db.String(20), default="local")
    google_id = db.Column(db.String(255))

    # ================= EMAIL VERIFICATION =================
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255))
    verification_token_expiry = db.Column(db.DateTime)
    email_verification_code = db.Column(db.String(6))
    email_verification_expiry = db.Column(db.DateTime)

    # ================= SECURITY =================
    reset_token = db.Column(db.String(255))
    reset_token_expiry = db.Column(db.DateTime)

    # ================= PROFILE =================
    bio = db.Column(db.Text, default="")
    location = db.Column(db.String(120), default="")
    is_private = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.Text)
    birthday = db.Column(db.Date)  # 🎂 Private birthday

    # ================= STATUS =================
    online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ================= RELATIONSHIPS =================
    messages_sent = db.relationship(
        "Message",
        foreign_keys="Message.sender_id",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # ================= AUTH =================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
