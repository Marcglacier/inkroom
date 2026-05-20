# app/auth/views/register.py
from flask.views import MethodView
from flask import request, jsonify
from app.extensions import db
from app.models.user import User
from app.models.profile import Profile
import re

print("REGISTER FILE LOADED")
class RegisterAPI(MethodView):
    print("🔥 REGISTER API ACTIVE VERSION 2.0")

    def post(self):
        d = request.get_json()

        username = (d.get("username") or "").strip()
        email = (d.get("email") or "").strip().lower()
        password = d.get("password") or ""
        is_private = d.get("is_private", False)

        # REQUIRED FIELDS
        if not username or not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        if len(username) < 3:
            return jsonify({"message": "Username too short"}), 400

        # STRICT EMAIL VALIDATION (FIXED)
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$"
        if not re.match(email_regex, email):
            return jsonify({"message": "Invalid email format"}), 400

        # STRONG PASSWORD RULE (STRICT)
        password_regex = (
            r"^(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r"[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.match(password_regex, password):
            return jsonify({
                "message": "Weak password: 8+ chars, upper, lower, number, symbol"
            }), 400

        # DUPLICATES
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already taken"}), 400

        # CREATE USER
        user = User(username=username, email=email, is_private=is_private)
        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        # CREATE PROFILE
        db.session.add(Profile(user_id=user.id, is_private=is_private))
        db.session.commit()

        return jsonify({
            "message": "Account created",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 201