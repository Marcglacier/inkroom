# app/models/follow_request.py
from datetime import datetime, timezone
from app.extensions import db


class FollowRequest(db.Model):
    __tablename__ = "follow_requests"

    id = db.Column(db.Integer, primary_key=True)

    requester_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    target_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "requester_id",
            "target_id",
            name="unique_follow_request",
        ),
        db.Index("idx_follow_request_target", "target_id"),
        db.Index("idx_follow_request_requester", "requester_id"),
    )