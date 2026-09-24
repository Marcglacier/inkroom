# app/auth/views/google/google.py
from flask.views import MethodView
from flask import current_app
from app.extensions import oauth


class GoogleAPI(MethodView):

    def get(self):
        redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]

        return oauth.google.authorize_redirect(
            redirect_uri,
            prompt="consent select_account"
        )