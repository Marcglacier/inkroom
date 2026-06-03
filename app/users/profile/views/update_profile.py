# app/users/profile/views/update_profile.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.profile.services.update_profile import update_profile


class UpdateProfileAPI(MethodView):
    @jwt_required()
    def patch(self):
        user_id = int(get_jwt_identity())

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = update_profile(user_id, data)

        return jsonify(result), 200