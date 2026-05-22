# app/auth/views/forgot_password.py
from flask.views import MethodView
from flask import request, jsonify
from datetime import datetime, timedelta
import secrets

from app.extensions import db
from app.models.user import User
from app.utils.mailer import send_email  # <-- import helper

class ForgotPasswordAPI(MethodView):
    def post(self):
        data = request.get_json()
        if not data or "email" not in data:
            return jsonify({"error": "Email required"}), 400

        email = data.get("email")
        user = User.query.filter_by(email=email).first()

        # Prevent email enumeration
        if not user:
            return jsonify({"message": "If that email exists, a reset link has been sent"}), 200

        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

        reset_url = f"http://localhost:5173/reset-password/{token}"

        # 🔥 Send gothic InkRoom email
        subject = "InkRoom – Reset Your Oath"
        body = f"""
Greetings from the InkRoom,

A request was made to reset your password.
Click the link below to forge a new oath:

{reset_url}

If you did not request this, ignore this raven.
"""
        send_email(to=email, subject=subject, body=body)

        return jsonify({"message": "If that email exists, a reset link has been sent"}), 200
