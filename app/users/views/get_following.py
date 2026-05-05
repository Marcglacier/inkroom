# app/users/views/get_followers.py
from flask.views import MethodView
from flask import jsonify

from app.users.services.follow_service import FollowService


class GetFollowingAPI(MethodView):

    def get(self, user_id):

        following = FollowService.get_following(user_id)

        return jsonify([
            {
                "following_id": f.following_id,
                "created_at": f.created_at
            }
            for f in following
        ])
    