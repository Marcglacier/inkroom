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
        email = data.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "If email exists, reset sent"})

        token = secrets.token_urlsafe(32)

        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

        db.session.commit()

        return jsonify({
            "message": "Reset token generated",
            "reset_token": token
        })