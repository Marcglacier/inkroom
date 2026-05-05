# app/auth/views/reset_password.py
from flask.views import MethodView
from flask import request, jsonify
from datetime import datetime

from app.extensions import db
from app.models.user import User


class ResetPasswordAPI(MethodView):

    def post(self):

        data = request.get_json()

        token = data.get("token")
        new_password = data.get("password")

        if not token or not new_password:
            return jsonify({"error": "Token and password required"}), 400

        user = User.query.filter_by(reset_token=token).first()

        if not user:
            return jsonify({"error": "Invalid token"}), 400

        if user.reset_token_expiry < datetime.utcnow():
            return jsonify({"error": "Token expired"}), 400

        user.set_password(new_password)

        # invalidate token after use
        user.reset_token = None
        user.reset_token_expiry = None

        db.session.commit()

        return jsonify({
            "message": "Password successfully reset"
        }), 200