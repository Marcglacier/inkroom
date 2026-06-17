# app/users/views/accept_follow.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.social.services import accept_follow


class AcceptFollowAPI(MethodView):

    @jwt_required()
    def post(self, user_id, follower_id):

        current_user_id = int(get_jwt_identity())

        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        result = accept_follow(
            user_id,
            follower_id
        )

        return jsonify(result), 200