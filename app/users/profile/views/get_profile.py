# app/users/profile/views/get_profile.py

from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.profile.services.get_profile import get_profile


class GetProfileAPI(MethodView):

    @jwt_required()
    def get(self, user_id):


        # ✅ AUTH USER
        viewer_id = int(get_jwt_identity())

        # ✅ FETCH PROFILE
        profile_data = get_profile(viewer_id, user_id)

        # detect empty values
        if not profile_data.get("social_links"):
            print("⚠️ NO SOCIAL LINKS RETURNED")

        if profile_data.get("social_links") == {}:
            print("⚠️ SOCIAL LINKS IS EMPTY OBJECT")

        if profile_data.get("social_links") == []:
            print("⚠️ SOCIAL LINKS IS EMPTY ARRAY")


        return jsonify(profile_data)