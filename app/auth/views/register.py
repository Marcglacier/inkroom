# app/auth/views/register.py
from flask.views import MethodView
from flask import request, jsonify
from app.extensions import db, mail
from app.models.user import User
from app.models.profile import Profile
from flask_mail import Message as MailMessage
import re, random
from datetime import datetime, timedelta
from app.utils.username import clean_username


class RegisterAPI(MethodView):

    def _generate_unique_username(self, base: str) -> str:
        username = clean_username(base)

        original = username
        counter = 1

        while User.query.filter_by(username=username).first():
            username = f"{original}{counter}"
            counter += 1

        return username

    def post(self):
        d = request.get_json()

        raw_username = d.get("username") or ""
        email = (d.get("email") or "").strip().lower()
        password = d.get("password") or ""
        is_private = d.get("is_private", False)

        if not email or not password:
            return jsonify({"message": "Email and password required"}), 400

        # clean username BEFORE validation
        username = self._generate_unique_username(raw_username or email.split("@")[0])

        email_re = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$"
        if not re.match(email_re, email):
            return jsonify({"message": "Invalid email"}), 400

        pwd_re = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pwd_re, password):
            return jsonify({"message": "Weak password"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email exists"}), 400

        # username uniqueness already handled, but keep safety check
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username exists"}), 400

        code = str(random.randint(100000, 999999))
        expiry = datetime.utcnow() + timedelta(minutes=10)

        user = User(
            username=username,
            email=email,
            is_private=is_private,
            email_verified=False,
            email_verification_code=code,
            email_verification_expiry=expiry,
            name=None
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        db.session.add(Profile(user_id=user.id, is_private=is_private, bio=None))
        db.session.commit()

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
            "username": username,
            "requires_verification": True
        }), 201