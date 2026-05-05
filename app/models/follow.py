# app/models/follow.py
from datetime import datetime
from app.extensions import db
from app.models import user


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "follower_id",
            "following_id",
            name="unique_user_follow"
        ),
        db.Index("idx_follower_id", "follower_id"),
        db.Index("idx_following_id", "following_id"),
    )

    status = db.Column(db.String(20), default="following")  # following | requested
