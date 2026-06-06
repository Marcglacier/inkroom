from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.social.services import unfollow_user


class UnfollowUserAPI(MethodView):

    @jwt_required()
    def post(self, user_id):  # 👈 CHANGE delete → post

        follower_id = int(get_jwt_identity())

        result = unfollow_user(follower_id, user_id)

        return jsonify({
            "message": result.get("message", "User unfollowed"),
            "status": "unfollowed",
            "follower_id": follower_id,
            "following_id": user_id
        }), 200