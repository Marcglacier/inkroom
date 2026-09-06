from datetime import datetime

from app.extensions import db


class MediaView(db.Model):
    __tablename__ = "media_views"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    media_id = db.Column(
        db.Integer,
        db.ForeignKey("message_media.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    opened_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref="media_views",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "media_id",
            "user_id",
            name="uq_media_user_view",
        ),
    )