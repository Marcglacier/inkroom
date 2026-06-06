from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.social.services.get_followers import get_followers
from app.users.social.services.relationship_service import get_relationship

from app.models.profile import Profile


class GetFollowersAPI(MethodView):

    @jwt_required()
    def get(self, user_id):

        current_user_id = int(get_jwt_identity())

        followers = get_followers(user_id)

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
                }
            }
            for u in followers
            for relationship in [get_relationship(current_user_id, u.id)]
        ])