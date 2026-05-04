# app/auth/views/reset_password.py

from flask.views import MethodView
from flask import request, jsonify
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.extensions import db
from app.models.user import User
from flask import current_app


class ResetPasswordAPI(MethodView):

    def post(self):
        data = request.get_json() or {}

        token = data.get("token")
        password = data.get("password")

        if not token or not password:
            return jsonify({"error": "Token and password required"}), 400

        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        try:
            email = serializer.loads(token, salt="reset-password", max_age=3600)
        except SignatureExpired:
            return jsonify({"error": "Token expired"}), 400
        except BadSignature:
            return jsonify({"error": "Invalid token"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.set_password(password)
        db.session.commit()

        return jsonify({"message": "Password reset successful"})