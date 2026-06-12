# app/models/follow_request.py
from datetime import datetime, timezone
from app.extensions import db


class FollowRequest(db.Model):
    __tablename__ = "follow_requests"

    id = db.Column(db.Integer, primary_key=True)

    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )