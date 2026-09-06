# app/users/social/views/reject_follow.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.social.actions.relationship_actions import (
    reject_follow_relationship,
)

class RejectFollowAPI(MethodView):

    @jwt_required()
    def post(self, user_id, follower_id):

        current_user_id = int(get_jwt_identity())

        # Only the owner of the request can reject it
        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        result = reject_follow_relationship(
            user_id,
            follower_id
        )

        if result == "request_not_found":
            return jsonify({
                "error": "Request not found"
            }), 404

        return jsonify({
            "message": "Follow request rejected",
            "status": "rejected",
            "follower_id": follower_id,
            "following_id": user_id,
        }), 200