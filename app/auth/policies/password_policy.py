# app/auth/policies/password_policy.py
import re
from flask import abort


class PasswordPolicy:

    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> str:
        if not password:
            abort(400, description="Password is required.")

        if len(password) < cls.MIN_LENGTH:
            abort(
                400,
                description="Password must be at least 8 characters.",
            )

        if not re.search(r"[a-z]", password):
            abort(
                400,
                description="Password must contain a lowercase letter.",
            )

        if not re.search(r"[A-Z]", password):
            abort(
                400,
                description="Password must contain an uppercase letter.",
            )

        if not re.search(r"\d", password):
            abort(
                400,
                description="Password must contain a number.",
            )

        if not re.search(r"[^A-Za-z0-9]", password):
            abort(
                400,
                description="Password must contain a special character.",
            )

        return password