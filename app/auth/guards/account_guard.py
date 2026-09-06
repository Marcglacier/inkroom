# app/auth/guards/account_guard.py
from flask import abort

from app.auth.resolvers.user_resolver import UserResolver


class AccountGuard:

    @staticmethod
    def require_email_available(email: str):

        user = UserResolver.by_email(email)

        if user:
            abort(
                409,
                description="An account with this email already exists.",
            )