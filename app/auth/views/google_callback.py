from flask.views import MethodView
from flask import redirect
from flask_jwt_extended import create_access_token
from app.extensions import oauth, db
from app.models.user import User
from app.utils.username import clean_username


class GoogleCallbackAPI(MethodView):

    def _generate_unique_username(self, base: str) -> str:
        """
        Ensure username is unique in DB
        """
        username = clean_username(base)

        original = username
        counter = 1

        while User.query.filter_by(username=username).first():
            username = f"{original}{counter}"
            counter += 1

        return username

    def get(self):
        google = oauth.google

        token = google.authorize_access_token()
        user_info = token["userinfo"]

        email = user_info["email"]
        raw_username = user_info.get("name") or user_info.get("email").split("@")[0]

        username = self._generate_unique_username(raw_username)

        user = User.query.filter_by(email=email).first()
        is_new = False

        if not user:
            user = User(
                email=email,
                username=username,
                google_id=user_info["sub"],
                email_verified=True,
                profile_completed=False
            )
            db.session.add(user)
            db.session.commit()
            is_new = True
        else:
            # FIX: ensure old users also get corrected usernames
            if not user.username:
                user.username = username
                db.session.commit()

        access_token = create_access_token(identity=str(user.id))

        return redirect(
            f"http://localhost:5173/oauth-success"
            f"?token={access_token}"
            f"&new={str(is_new).lower()}"
        )