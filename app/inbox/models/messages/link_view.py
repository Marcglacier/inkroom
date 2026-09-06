# app/inbox/models/messages/link_view.py
from datetime import datetime

from app.extensions import db


class LinkView(db.Model):
    __tablename__ = "link_views"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    link_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "message_links.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
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
        backref="link_views",
    )

    link = db.relationship(
        "MessageLink",
        backref="views",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "link_id",
            "user_id",
            name="uq_link_user_view",
        ),
    )