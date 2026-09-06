# app/auth/views/google_callback.py

from flask.views import MethodView
from flask import redirect, current_app
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer

from app.extensions import oauth, db
from app.models.user import User
from app.models.pending_google_registration import PendingGoogleRegistration


class GoogleCallbackAPI(MethodView):

    def get(self):
        google = oauth.google

        token = google.authorize_access_token()
        user_info = token["userinfo"]

        email = user_info["email"]
        google_id = user_info["sub"]

        # --------------------------------------------------
        # 1. EXISTING GOOGLE USER
        # --------------------------------------------------

        user = User.query.filter_by(
            google_id=google_id
        ).first()

        if user:
            access_token = create_access_token(
                identity=str(user.id)
            )

            return redirect(
                f"http://localhost:5173/oauth-success"
                f"?token={access_token}"
                f"&new=false"
            )

        # --------------------------------------------------
        # 2. EXISTING ACCOUNT WITH SAME EMAIL
        # --------------------------------------------------

        user = User.query.filter_by(
            email=email
        ).first()

        if user:
            return redirect(
                "http://localhost:5173/login"
                "?error=account_exists"
            )

        # --------------------------------------------------
        # 3. CREATE / UPDATE PENDING GOOGLE REGISTRATION
        # --------------------------------------------------

        pending = PendingGoogleRegistration.query.filter_by(
            google_id=google_id
        ).first()

        if pending:
            pending.email = email

        else:
            pending = PendingGoogleRegistration(
                google_id=google_id,
                email=email,
            )

            db.session.add(pending)

        db.session.commit()

        # --------------------------------------------------
        # 4. CREATE SHORT-LIVED ONBOARDING TOKEN
        # --------------------------------------------------

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        onboarding_token = serializer.dumps({
            "pending_id": pending.id,
            "google_id": google_id,
        })
        print("🔥 GOOGLE ONBOARDING TOKEN:", onboarding_token)
        print("🔥 PENDING ID:", pending.id)
        print("🔥 GOOGLE ID:", google_id)
        # --------------------------------------------------
        # 5. SEND USER TO CHOOSE USERNAME
        # --------------------------------------------------

        return redirect(
            "http://localhost:5173/choose-username"
            f"?token={onboarding_token}"
        )