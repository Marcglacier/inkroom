# app/models/profile.py
from datetime import datetime
from app.extensions import db
from sqlalchemy.dialects.postgresql import JSON

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    bio = db.Column(db.String(280), default="")
    location = db.Column(db.String(100), default="")
    birthday = db.Column(db.Date, nullable=True)
    avatar_url = db.Column(db.String(255), default="")
    cover_url = db.Column(db.String(255), default="")
    is_private = db.Column(db.Boolean, default=False, nullable=False)

    # 🎯 Flexible social links
    social_links = db.Column(JSON, default={})

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
