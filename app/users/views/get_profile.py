# app/users/views/get_profile.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.services.profile_service import get_profile


class GetProfileAPI(MethodView):

    @jwt_required()
    def get(self, user_id):

        viewer_id = int(get_jwt_identity())

        profile = get_profile(viewer_id, user_id)

        return jsonify(profile)
    