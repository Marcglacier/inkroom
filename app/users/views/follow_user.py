# app/users/views/follow_user.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.services.follow_service import FollowService


class FollowUserAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        follower_id = int(get_jwt_identity())

        try:
            created = FollowService.follow_user(
                follower_id,
                user_id
            )

            if not created:
                return jsonify({
                    "message": "Already following"
                }), 200

            return jsonify({
                "message": "User followed"
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400