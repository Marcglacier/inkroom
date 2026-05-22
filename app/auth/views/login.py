# app/auth/views/login.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app.models.user import User


class LoginAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        if not user.email_verified:
            return jsonify({"message": "Please verify your email first"}), 403

        token = create_access_token(identity=str(user.id))
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }), 200
