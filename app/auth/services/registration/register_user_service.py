# app/auth/services/registration/register_user_service.py
import secrets
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app.extensions import db

from app.auth.guards import (
    AccountGuard,
    UsernameGuard,
)

from app.auth.policies import (
    EmailPolicy,
    PasswordPolicy,
    UsernamePolicy,
)

from app.auth.resolvers import (
    PendingRegistrationResolver,
)

from app.models.pending_registration import PendingRegistration


class RegisterUserService:

    VERIFICATION_CODE_EXPIRY_MINUTES = 10

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        is_private: bool = False,
    ):
        self.username = username
        self.email = email
        self.password = password
        self.is_private = bool(is_private)

    def execute(self):

        # ================= VALIDATION =================

        username = UsernamePolicy.validate(
            self.username
        )

        email = EmailPolicy.normalize(
            self.email
        )

        PasswordPolicy.validate(
            self.password
        )

        # ================= ACTIVE ACCOUNT =================

        AccountGuard.require_email_available(
            email
        )

        # ================= PENDING REGISTRATION =================

        pending = (
            PendingRegistrationResolver.by_email(
                email
            )
        )

        # ================= EXPIRED PENDING =================

        if pending and self._is_expired(pending):

            db.session.delete(pending)
            db.session.flush()

            pending = None

        # ================= USERNAME AVAILABILITY =================

        UsernameGuard.require_available(
            username,
            exclude_pending_id=(
                pending.id
                if pending
                else None
            ),
        )

        # ================= HANDLE EXISTING PENDING =================

        if pending:

            # Same email, but user wants
            # a different username.
            #
            # The old pending registration
            # is replaced.

            if pending.username != username:

                db.session.delete(pending)
                db.session.flush()

                pending = None

        # ================= VERIFICATION =================

        verification_code = (
            self._generate_verification_code()
        )

        verification_expires_at = (
            datetime.utcnow()
            + timedelta(
                minutes=self.VERIFICATION_CODE_EXPIRY_MINUTES
            )
        )

        verification_code_hash = (
            generate_password_hash(
                verification_code
            )
        )

        # ================= CREATE / UPDATE =================

        if pending:

            pending.password_hash = (
                generate_password_hash(
                    self.password
                )
            )

            pending.is_private = self.is_private

            pending.verification_code_hash = (
                verification_code_hash
            )

            pending.verification_expires_at = (
                verification_expires_at
            )

        else:

            pending = PendingRegistration(
                username=username,
                email=email,
                password_hash=(
                    generate_password_hash(
                        self.password
                    )
                ),
                is_private=self.is_private,
                verification_code_hash=(
                    verification_code_hash
                ),
                verification_expires_at=(
                    verification_expires_at
                ),
            )

            db.session.add(pending)

        # ================= PERSIST =================

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()
            raise

        # ================= SEND VERIFICATION =================


        # ================= RESULT =================

        return {
            "email": email,
            "username": username,
            "verification_code": verification_code,
            "requires_verification": True,
        }

    @classmethod
    def _generate_verification_code(cls) -> str:

        return f"{secrets.randbelow(1_000_000):06d}"

    @staticmethod
    def _is_expired(
        pending: PendingRegistration,
    ) -> bool:

        return (
            pending.verification_expires_at
            <= datetime.utcnow()
        )