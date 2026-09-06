# app/auth/policies/email_policy.py
import re
from flask import abort


class EmailPolicy:

    PATTERN = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
    )

    @classmethod
    def normalize(cls, email: str) -> str:
        email = (email or "").strip().lower()

        if not email:
            abort(400, description="Email is required.")

        if not cls.PATTERN.fullmatch(email):
            abort(400, description="Invalid email address.")

        return email