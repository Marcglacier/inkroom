# app/users/views/reject_follow.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.services.follow_service import FollowService


class RejectFollowAPI(MethodView):

    @jwt_required()
    def post(self, user_id, follower_id):

        current_user_id = int(get_jwt_identity())

        # ensure only owner can reject
        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        result = FollowService.reject_follow(user_id, follower_id)

        if isinstance(result, tuple):
            data, code = result
            return jsonify(data), code

        return jsonify(result), 200