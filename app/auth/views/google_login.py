# app/auth/views/google_login.py
from flask import redirect, url_for
from flask.views import MethodView
from app.extensions import oauth

class GoogleLoginAPI(MethodView):

    def get(self):

        google = oauth.create_client("google")

        redirect_uri = url_for(
            "auth.google_callback",
            _external=True
        )

        return google.authorize_redirect(redirect_uri)