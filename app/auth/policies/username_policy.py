# app/auth/policies/username_policy.py

import re
from flask import abort


class UsernamePolicy:

    MIN_LENGTH = 6
    MAX_LENGTH = 30

    # lowercase letters, numbers, underscores, and dots
    PATTERN = re.compile(r"^[a-z0-9_.]+$")

    @classmethod
    def validate(cls, username: str) -> str:

        username = (username or "").strip()

        # ================= REQUIRED =================

        if not username:
            abort(
                400,
                description="Username is required.",
            )

        # ================= LENGTH =================

        if len(username) < cls.MIN_LENGTH:
            abort(
                400,
                description="Username must be at least 6 characters.",
            )

        if len(username) > cls.MAX_LENGTH:
            abort(
                400,
                description="Username must not exceed 30 characters.",
            )

        # ================= CASE =================

        if username != username.lower():
            abort(
                400,
                description="Username must contain lowercase characters only.",
            )

        # ================= CHARACTERS =================

        if not cls.PATTERN.fullmatch(username):
            abort(
                400,
                description=(
                    "Username may contain only lowercase letters, "
                    "numbers, underscores, and dots."
                ),
            )

        # ================= DOT RULES =================

        if username.startswith(".") or username.endswith("."):
            abort(
                400,
                description="Username cannot start or end with a dot.",
            )

        if ".." in username:
            abort(
                400,
                description="Username cannot contain consecutive dots.",
            )

        return username