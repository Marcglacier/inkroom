# app/models/follow.py

from datetime import datetime, timezone
from app.extensions import db


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    follower = db.relationship(
        "User",
        foreign_keys=[follower_id],
        backref="following_relationships",
    )

    following = db.relationship(
        "User",
        foreign_keys=[following_id],
        backref="follower_relationships",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "follower_id",
            "following_id",
            name="unique_user_follow",
        ),
        db.Index("idx_follower_id", "follower_id"),
        db.Index("idx_following_id", "following_id"),
    )