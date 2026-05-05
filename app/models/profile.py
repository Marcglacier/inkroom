# app/models/profile.py
from datetime import datetime
from app.extensions import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    bio = db.Column(
        db.String(280),
        default=""
    )

    location = db.Column(
        db.String(100),
        default=""
    )

    avatar_url = db.Column(
        db.String(255),
        default=""
    )

    is_private = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )