from flask.views import MethodView
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.extensions import db
from app.models.user import User
from app.models.pending_google_registration import PendingGoogleRegistration
from app.utils.username import clean_username


class GoogleCompleteAPI(MethodView):

    def post(self):
        data = request.get_json() or {}

        username = clean_username(data.get("username"))
        onboarding_token = data.get("token")

        # --------------------------------------------------
        # VALIDATE USERNAME
        # --------------------------------------------------

        if not username:
            return jsonify({
                "error": "Username is required"
            }), 400

        if len(username) < 6:
            return jsonify({
                "error": "Username must be at least 6 characters"
            }), 400

        # --------------------------------------------------
        # VALIDATE ONBOARDING TOKEN
        # --------------------------------------------------

        if not onboarding_token:
            return jsonify({
                "error": "Google registration session is missing"
            }), 400

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        try:
            payload = serializer.loads(
                onboarding_token,
                max_age=600,  # 10 minutes
            )

        except SignatureExpired:
            return jsonify({
                "error": "Google registration session expired"
            }), 401

        except BadSignature:
            return jsonify({
                "error": "Invalid Google registration session"
            }), 401

        pending_id = payload.get("pending_id")
        google_id = payload.get("google_id")

        if not pending_id or not google_id:
            return jsonify({
                "error": "Invalid Google registration session"
            }), 400

        # --------------------------------------------------
        # GET PENDING GOOGLE REGISTRATION
        # --------------------------------------------------

        pending = PendingGoogleRegistration.query.get(
            pending_id
        )

        if not pending:
            return jsonify({
                "error": "Google registration session expired"
            }), 404

        # --------------------------------------------------
        # VERIFY TOKEN MATCHES PENDING REGISTRATION
        # --------------------------------------------------

        if pending.google_id != google_id:
            return jsonify({
                "error": "Google registration session is invalid"
            }), 401

        # --------------------------------------------------
        # VALIDATE USERNAME
        # --------------------------------------------------

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return jsonify({
                "error": "Username is already taken"
            }), 409

        # --------------------------------------------------
        # DOUBLE-CHECK EMAIL
        # --------------------------------------------------

        if User.query.filter_by(
            email=pending.email
        ).first():

            return jsonify({
                "error": "An account with this email already exists"
            }), 409

        # --------------------------------------------------
        # DOUBLE-CHECK GOOGLE IDENTITY
        # --------------------------------------------------

        if User.query.filter_by(
            google_id=pending.google_id
        ).first():

            return jsonify({
                "error": "This Google account is already registered"
            }), 409

        # --------------------------------------------------
        # CREATE USER
        # --------------------------------------------------

        user = User(
            username=username,
            email=pending.email,
            google_id=pending.google_id,
            provider="google",
            email_verified=True,
            profile_completed=False,
        )

        db.session.add(user)

        # Pending registration has served its purpose.
        db.session.delete(pending)

        db.session.commit()

        # --------------------------------------------------
        # ISSUE JWT
        # --------------------------------------------------

        access_token = create_access_token(
            identity=str(user.id)
        )

        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_completed": user.profile_completed,
            }
        }), 201