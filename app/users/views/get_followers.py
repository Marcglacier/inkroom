# app/users/views/get_followers.py
from flask.views import MethodView
from flask import jsonify

from app.users.services import get_followers


class GetFollowersAPI(MethodView):

    def get(self, user_id):

        followers = get_followers(user_id)

        return jsonify([
            {
                "follower_id": f.follower_id,
                "created_at": f.created_at
            }
            for f in followers
        ])