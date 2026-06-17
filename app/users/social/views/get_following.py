from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.social.services.get_following import get_following
from app.users.social.services.relationship_service import get_relationship

from app.models.profile import Profile


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
                    Profile.query.filter_by(user_id=u.id)
                    .first()
                    .avatar_url
                    if Profile.query.filter_by(user_id=u.id).first()
                    else None
                ),

                **{
                    "is_following": relationship["following"],
                    "is_followed_by": relationship["followed_back"],
                    "relationship": relationship["state"],
                    "is_mutual": relationship["is_mutual"],

                    # 🔥 NEW
                    "has_sent_request": relationship["has_sent_request"],
                    "has_received_request": relationship["has_received_request"],
                }
            }
            for u in following
            for relationship in [get_relationship(current_user_id, u.id)]
        ])