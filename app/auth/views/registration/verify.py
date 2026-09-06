# app/auth/views/registration/verify.py
from flask.views import MethodView
from flask import request, jsonify

from app.auth.services import VerifyRegistrationService


class VerifyRegistrationAPI(MethodView):

    def post(self):

        data = request.get_json() or {}

        result = VerifyRegistrationService(
            email=data.get("email"),
            verification_code=data.get(
                "verification_code"
            ),
        ).execute()

        user = result["user"]

        return jsonify({
            "message": (
                "Email verified. "
                "Account created successfully."
            ),
            "email": user.email,
            "username": user.username,
            "email_verified": user.email_verified,
        }), 201