from flask.views import MethodView
from flask import redirect
from flask_jwt_extended import create_access_token

from app.extensions import oauth, db
from app.models.user import User


class GoogleCallbackAPI(MethodView):

    def get(self):
        google = oauth.google

        token = google.authorize_access_token()
        user_info = token["userinfo"]

        email = user_info["email"]
        username = user_info["name"]

        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(
                email=email,
                username=username,
                google_id=user_info["sub"],
                email_verified=True
            )
            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=str(user.id))

        # 🔥 REDIRECT WITH TOKEN (CRITICAL
        return redirect(
    f"http://localhost:5173/oauth-success?token={access_token}"
     )