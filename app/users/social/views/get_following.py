# app/users/social/views/get_following.py

from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.storage.service import get_file_url
from app.users.social.services.get_following import get_following
from app.users.social.services.relationship_service import get_relationship


class GetFollowingAPI(MethodView):

    @jwt_required()
    def get(self, user_id):

        current_user_id = int(get_jwt_identity())

        following = get_following(user_id)

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "name": u.name,

                "avatar_url": (
                    get_file_url(u.profile_picture)
                    if u.profile_picture
                    else None
                ),

                "is_following": relationship["following"],
                "is_followed_by": relationship["followed_by"],
                "relationship": relationship["state"],
                "is_mutual": relationship["is_mutual"],
                "has_sent_request": relationship["request_sent"],
                "has_received_request": relationship["request_received"],
            }
            for u in following
            for relationship in [get_relationship(current_user_id, u.id)]
        ])