# app/users/social/views/follow_user.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.social.actions.relationship_actions import follow_relationship
class FollowUserAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        viewer_id = int(get_jwt_identity())

        result = follow_relationship(
            viewer_id,
            user_id
        )

        # service returned (payload, status_code)
        if result == "requested":
            return jsonify({"status": result}), 202

        if result == "following":
            return jsonify({"status": result}), 201

        if result == "already_following":
            return jsonify({"status": result}), 200

        if result == "request_exists":
            return jsonify({"status": result}), 200

        return jsonify({"status": result}), 200