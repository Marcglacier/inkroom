# app/models/notification_settings.py

from datetime import datetime

from app.extensions import db


class NotificationSettings(db.Model):
    __tablename__ = "notification_settings"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    muted_until = db.Column(
        db.DateTime,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "notification_settings",
            uselist=False,
            cascade="all, delete-orphan",
        ),
    )

    @property
    def is_muted(self):
        if not self.muted_until:
            return False

        return self.muted_until > datetime.utcnow()