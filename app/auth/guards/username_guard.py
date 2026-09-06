# app/auth/guards/username_guard.py
from flask import abort
from app.auth.resolvers import (
   UserResolver, PendingRegistrationResolver,
)


class UsernameGuard:

    @staticmethod
    def require_available(
        username: str,
        exclude_pending_id: int | None = None,
    ):

        user = UserResolver.by_username(
            username
        )

        if user:
            abort(
                409,
                description="Username already taken.",
            )

        pending = (
            PendingRegistrationResolver.by_username(
                username
            )
        )

        if (
            pending
            and pending.id != exclude_pending_id
        ):
            abort(
                409,
                description="Username is currently reserved.",
            )
        