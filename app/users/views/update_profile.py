# app/users/views/update_profile.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.services.profile_service import update_profile, get_profile


class UpdateProfileAPI(MethodView):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        result = get_profile(user_id, user_id)

        return jsonify(result), 200


    @jwt_required()
    def patch(self):
        user_id = int(get_jwt_identity())

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = update_profile(user_id, data)

        return jsonify(result), 200