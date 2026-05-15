# app/users/views/unfollow_user.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.services import unfollow_user


class UnfollowUserAPI(MethodView):

    @jwt_required()
    def delete(self, user_id):

        follower_id = int(get_jwt_identity())

        deleted = unfollow_user(
            follower_id,
            user_id
        )

        if not deleted:
            return jsonify({
                "message": "Not following"
            }), 404

        return jsonify({
            "message": "User unfollowed"
        })