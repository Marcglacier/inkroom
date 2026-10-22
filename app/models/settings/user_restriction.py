# app/models/settings/user_restriction.py
from datetime import datetime

from app.extensions import db


class UserRestriction(db.Model):
    __tablename__ = "user_restrictions"

    id = db.Column(db.Integer, primary_key=True)

    restricter_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    restricted_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "restricter_id",
            "restricted_id",
            name="uq_user_restriction_pair",
        ),
        db.CheckConstraint(
            "restricter_id != restricted_id",
            name="ck_user_restriction_not_self",
        ),
    )