# app/models/pending_registration.py
from datetime import datetime

from app.extensions import db


class PendingRegistration(db.Model):
    __tablename__ = "pending_registrations"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # ================= REGISTRATION IDENTITY =================

    username = db.Column(
        db.String(30),
        nullable=False,
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        index=True,
    )

    # ================= CREDENTIALS =================

    password_hash = db.Column(
        db.Text,
        nullable=False,
    )

    # ================= ACCOUNT OPTIONS =================

    is_private = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    # ================= EMAIL VERIFICATION =================

    verification_code_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    verification_expires_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    # ================= TIMESTAMPS =================

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