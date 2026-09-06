# app/auth/views/registration/register.py
from flask.views import MethodView
from flask import request, jsonify

from app.auth.services import StartRegistrationService


class RegisterAPI(MethodView):

    def post(self):

        data = request.get_json() or {}

        result = StartRegistrationService(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            is_private=data.get(
                "is_private",
                False,
            ),
        ).execute()

        return jsonify({
            "message": (
                "Registration started. "
                "Check your email."
            ),
            "email": result["email"],
            "username": result["username"],
            "requires_verification": True,
        }), 201