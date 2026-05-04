# chat.py
from datetime import datetime
from app.extensions import db


class ChatRoom(db.Model):
    __tablename__ = "chat_rooms"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


