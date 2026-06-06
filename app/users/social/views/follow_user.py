# app/users/social/views/follow_user.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.social.services import follow_user


class FollowUserAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        viewer_id = int(get_jwt_identity())

        result = follow_user(
            viewer_id,
            user_id
        )

        # service returned (payload, status_code)
        if isinstance(result, tuple):
            payload, status_code = result
            return jsonify(payload), status_code

        status = result.get("status")

        if status == "requested":
            return jsonify(result), 202

        if status == "following":
            return jsonify(result), 201

        # NEW: toggle unfollow response
        if status == "unfollowed":
            return jsonify(result), 200

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200