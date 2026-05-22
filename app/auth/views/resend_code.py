# app/auth/views/resend_code.py
import random
from datetime import datetime, timedelta
from flask.views import MethodView
from flask import request, jsonify
from flask_mail import Message as MailMessage

from app.extensions import db, mail
from app.models.user import User


class ResendCodeAPI(MethodView):

    def post(self):
        data = request.get_json()

        email = (data.get("email") or "").strip().lower()

        if not email:
            return jsonify({"message": "Email required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if user.email_verified:
            return jsonify({"message": "Already verified"}), 400

        # ================= ANTI-SPAM COOLDOWN =================
        if user.email_verification_expiry:
            remaining = (user.email_verification_expiry - datetime.utcnow()).total_seconds()
            if remaining > 540:
                return jsonify({"message": "Please wait before requesting another code"}), 429

        # ================= GENERATE NEW CODE =================
        code = str(random.randint(100000, 999999))

        user.email_verification_code = code
        user.email_verification_expiry = datetime.utcnow() + timedelta(minutes=10)

        db.session.commit()

        # ================= SEND EMAIL =================
        mail.send(MailMessage(
            subject="InkRoom Verification Code",
            sender="InkRoom <noreply@inkroom.app>",
            recipients=[email],
            body=f"Your new verification code is: {code}\nExpires in 10 minutes."
        ))

        return jsonify({
            "message": "New verification code sent",
            "email": email
        }), 200