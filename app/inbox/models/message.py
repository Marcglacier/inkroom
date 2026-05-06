# app/inbox/models/message.py

from datetime import datetime
from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # EDITING
    # =========================
    edited = db.Column(db.Boolean, default=False)

    # =========================
    # DELIVERY SYSTEM (WHATSAPP CORE)
    # =========================
    status = db.Column(db.String(20), default="sent")  # sent | delivered | read

    delivered_at = db.Column(db.DateTime, nullable=True)
    read_at = db.Column(db.DateTime, nullable=True)

    # =========================
    # DELETE SYSTEM
    # =========================
    deleted_for_everyone = db.Column(db.Boolean, default=False)
    deleted_for_users = db.Column(db.JSON, default=list)

    delete_requested_at = db.Column(db.DateTime, nullable=True)