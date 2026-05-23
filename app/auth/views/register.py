# app/auth/views/register.py

from flask.views import MethodView
from flask import request, jsonify
from app.extensions import db, mail
from app.models.user import User
from app.models.profile import Profile
from flask_mail import Message as MailMessage
import re, random
from datetime import datetime, timedelta


class RegisterAPI(MethodView):

    def post(self):
        d = request.get_json()

        username = (d.get("username") or "").strip()
        email = (d.get("email") or "").strip().lower()
        password = d.get("password") or ""
        is_private = d.get("is_private", False)

        if not username or not email or not password:
            return jsonify({"message": "All fields required"}), 400

        if len(username) < 3:
            return jsonify({"message": "Username too short"}), 400

        email_re = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$"
        if not re.match(email_re, email):
            return jsonify({"message": "Invalid email"}), 400

        pwd_re = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pwd_re, password):
            return jsonify({"message": "Weak password"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email exists"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username exists"}), 400

        # ================= CREATE USER =================
        code = str(random.randint(100000, 999999))
        expiry = datetime.utcnow() + timedelta(minutes=10)

        user = User(
            username=username,
            email=email,
            is_private=is_private,
            email_verified=False,
            email_verification_code=code,
            email_verification_expiry=expiry,
            name=None  # 👑 leave blank so frontend detects incomplete scroll
        )
        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        # 👑 create profile with empty bio
        db.session.add(Profile(user_id=user.id, is_private=is_private, bio=None))
        db.session.commit()

        # ================= SEND EMAIL =================
        msg = MailMessage(
            subject="InkRoom Verification Code",
            sender="InkRoom <noreply@inkroom.app>",
            recipients=[email],
            body=f"Your InkRoom verification code is: {code}\nExpires in 10 minutes."
        )
        mail.send(msg)

        return jsonify({
            "message": "Account created. Verify email.",
            "email": email,
            "requires_verification": True
        }), 201
