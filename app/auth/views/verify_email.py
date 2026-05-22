# api/auth/views/verify_email.py
from flask.views import MethodView
from flask import request, jsonify
from app.models.user import User
from app.extensions import db
from datetime import datetime


class VerifyEmailAPI(MethodView):

    def post(self):
        data = request.get_json()

        email = (data.get("email") or "").strip().lower()
        code = (data.get("code") or "").strip()

        # ================= VALIDATION =================
        if not email or not code:
            return jsonify({"message": "Email and code required"}), 400

        if len(code) != 6 or not code.isdigit():
            return jsonify({"message": "Invalid code format"}), 400

        # ================= FIND USER =================
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # already verified
        if user.email_verified:
            return jsonify({"message": "Email already verified"}), 200

        # ================= CHECK CODE =================
        if not user.email_verification_code:
            return jsonify({"message": "No verification code found"}), 400

        # expiry check
        if user.email_verification_expiry and datetime.utcnow() > user.email_verification_expiry:
            return jsonify({"message": "Code expired. Request new one"}), 400

        # wrong code
        if user.email_verification_code != code:
            return jsonify({"message": "Incorrect verification code"}), 400

        # ================= VERIFY USER =================
        user.email_verified = True
        user.email_verification_code = None
        user.email_verification_expiry = None

        db.session.commit()

        return jsonify({
            "message": "Email verified successfully",
            "email": user.email,
            "verified": True
        }), 200