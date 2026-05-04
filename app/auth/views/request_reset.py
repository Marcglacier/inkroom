# app/auth/views/request_reset.py

from flask.views import MethodView
from flask import request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer

from app.models.user import User


class RequestResetAPI(MethodView):

    def post(self):
        data = request.get_json() or {}
        email = data.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        token = serializer.dumps(email, salt="reset-password")

        return jsonify({
            "message": "Reset token generated",
            "token": token
        })