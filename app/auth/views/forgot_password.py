# app/auth/views/forgot_password.py
from flask.views import MethodView
from flask import request, jsonify
from datetime import datetime, timedelta
import secrets

from app.extensions import db
from app.models.user import User


class ForgotPasswordAPI(MethodView):

    def post(self):

        data = request.get_json()

        if not data or "email" not in data:
            return jsonify({"error": "Email required"}), 400

        email = data.get("email")

        user = User.query.filter_by(email=email).first()

        # Prevent email enumeration
        if not user:
            return jsonify({
                "message": "If that email exists, a reset link has been sent"
            }), 200

        token = secrets.token_urlsafe(32)

        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

        db.session.commit()

        # Later this becomes an email link
        reset_url = f"http://localhost:3000/reset-password?token={token}"

        return jsonify({
            "message": "Password reset link generated",
            "reset_token": token,
            "reset_url": reset_url
        }), 200