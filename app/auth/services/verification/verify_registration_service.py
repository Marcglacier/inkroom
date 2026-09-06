# app/auth/services/registration/verify_registration_service.py
from datetime import datetime

from flask import abort
from werkzeug.security import check_password_hash

from app.extensions import db

from app.auth.resolvers import (
    PendingRegistrationResolver,
)

from app.models.profile import Profile
from app.models.user import User


class VerifyRegistrationService:

    def __init__(
        self,
        email: str,
        verification_code: str,
    ):
        self.email = (email or "").strip().lower()
        self.verification_code = (
            verification_code or ""
        ).strip()

    def execute(self):

        # ================= INPUT =================

        if not self.email:
            abort(
                400,
                description="Email is required.",
            )

        if (
            not self.verification_code
            or len(self.verification_code) != 6
            or not self.verification_code.isdigit()
        ):
            abort(
                400,
                description="Invalid verification code.",
            )

        # ================= FIND PENDING =================

        pending = (
            PendingRegistrationResolver.by_email(
                self.email
            )
        )

        if not pending:
            abort(
                404,
                description=(
                    "No pending registration found."
                ),
            )

        # ================= EXPIRY =================

        if (
            pending.verification_expires_at
            <= datetime.utcnow()
        ):

            db.session.delete(pending)
            db.session.commit()

            abort(
                400,
                description=(
                    "Verification code expired. "
                    "Please register again."
                ),
            )

        # ================= CODE =================

        if not check_password_hash(
            pending.verification_code_hash,
            self.verification_code,
        ):
            abort(
                400,
                description="Incorrect verification code.",
            )

        # ================= FINAL ACCOUNT SAFETY =================

        existing_user = (
            User.query
            .filter(
                (User.email == pending.email)
                | (
                    User.username
                    == pending.username
                )
            )
            .first()
        )

        if existing_user:
            abort(
                409,
                description=(
                    "An account with these "
                    "credentials already exists."
                ),
            )

        # ================= CREATE USER =================

        user = User(
            username=pending.username,
            email=pending.email,
            is_private=pending.is_private,
            email_verified=True,
            name=None,
        )

        user.password_hash = (
            pending.password_hash
        )
        db.session.add(user)
        db.session.flush()
        # ================= CREATE PROFILE =================

        profile = Profile(
            user_id=user.id,
            is_private=pending.is_private,
        )

        
        db.session.add(profile)

        # ================= REMOVE PENDING =================

        db.session.delete(pending)

        # ================= TRANSACTION =================

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()
            raise

        return {
            "user": user,
            "profile": profile,
        }