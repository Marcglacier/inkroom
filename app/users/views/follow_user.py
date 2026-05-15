# app/users/views/follow_user.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.services import follow_user


class FollowUserAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        current_user_id = int(get_jwt_identity())

        result = follow_user(
            current_user_id,
            user_id
        )

        # =========================
        # ERROR HANDLING (SERVICE RETURNS TUPLES)
        # =========================
        if isinstance(result, tuple):
            data, code = result
            return jsonify(data), code

        # =========================
        # RESPONSE STATUS LOGIC
        # =========================
        status = result.get("status")

        if status == "requested":
            return jsonify(result), 202   # accepted for processing

        if status == "following":
            return jsonify(result), 201   # created relationship

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200