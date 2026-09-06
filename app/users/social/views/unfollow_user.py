from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.social.actions.relationship_actions import (
    unfollow_relationship,
)
class UnfollowUserAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        follower_id = int(get_jwt_identity())

        result = unfollow_relationship(
            follower_id,
            user_id
        )

        return jsonify({
            "message": "User unfollowed",
            "status": result,
            "follower_id": follower_id,
            "following_id": user_id,
        }), 200