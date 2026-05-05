# app/users/views/get_followers.py
from flask.views import MethodView
from flask import jsonify

from app.users.services.follow_service import FollowService


class GetFollowersAPI(MethodView):

    def get(self, user_id):

        followers = FollowService.get_followers(user_id)

        return jsonify([
            {
                "follower_id": f.follower_id,
                "created_at": f.created_at
            }
            for f in followers
        ])