# app/auth/views/google.py
from flask.views import MethodView
from flask import url_for
from app.extensions import oauth


class GoogleAPI(MethodView):

    def get(self):
        redirect_uri = url_for("auth.google_callback", _external=True)
        return oauth.google.authorize_redirect(redirect_uri)