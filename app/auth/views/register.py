# app/auth/views/register.py
from flask.views import MethodView
from flask import request, jsonify

from app.extensions import db
from app.models.user import User


class RegisterAPI(MethodView):

    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        is_private = data.get("is_private", False)  # 🔥 ADD THIS

        if not all([username, email, password]):
            return jsonify({"error": "Missing fields"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email exists"}), 400

        user = User(
            username=username,
            email=email,
            is_private=is_private   # 🔥 CRITICAL FIX
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User created",
            "user": {
                "id": user.id,
                "username": user.username,
                "is_private": user.is_private
            }
        }), 201