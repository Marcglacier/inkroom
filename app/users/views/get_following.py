from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.services.get_following import get_following

from app.models.follow import Follow
from app.models.profile import Profile


class GetFollowingAPI(MethodView):

    def _get_follow_state(self, current_user_id, target_user_id):

        follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=target_user_id
        ).first()

        if not follow:
            return "none"

        return follow.status or "none"

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

                "follow_state": self._get_follow_state(
                    current_user_id,
                    u.id
                )
            }
            for u in following
        ])