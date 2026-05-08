# app/inbox/models/conversation.py
from datetime import datetime
from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # keep ONLY if you already added them in DB
    status = db.Column(db.String, default="active")
    type = db.Column(db.String, default="dm")
    deleted_at = db.Column(db.DateTime, nullable=True)