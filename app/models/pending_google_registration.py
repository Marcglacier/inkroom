from datetime import datetime

from app.extensions import db


class PendingGoogleRegistration(db.Model):
    __tablename__ = "pending_google_registrations"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # ================= GOOGLE IDENTITY =================

    google_id = db.Column(
        db.String(255),
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
        index=True,
    )

    # ================= TIMESTAMP =================

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