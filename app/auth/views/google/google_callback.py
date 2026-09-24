# app/auth/views/google/google_callback.py

from flask.views import MethodView
from flask import redirect, current_app, request
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer

from app.extensions import oauth, db
from app.models.user import User
from app.models.pending_google_registration import PendingGoogleRegistration


class GoogleCallbackAPI(MethodView):

    def get(self):
        google = oauth.google
        frontend_url = f"{request.scheme}://{request.host.split(':')[0]}:5173"

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
                f"{frontend_url}/oauth-success"
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
                f"{frontend_url}/login"
                f"?error=account_exists"
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
            f"{frontend_url}/choose-username"
            f"?token={onboarding_token}"
        )