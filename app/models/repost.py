# app/models/repost.py

from datetime import datetime
from app.extensions import db


class Repost(db.Model):
    __tablename__ = "reposts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ ADD THIS (CRITICAL FIX)
    user = db.relationship(
        "User",
        backref=db.backref("reposts", lazy=True)
    )