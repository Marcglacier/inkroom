# notification.py
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    type = db.Column(db.String(50))

    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)