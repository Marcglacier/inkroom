# app/users/views/get_followers.py
from flask.views import MethodView
from flask import jsonify

from app.users.services import get_following


class GetFollowingAPI(MethodView):

    def get(self, user_id):

        following = get_following(user_id)

        return jsonify([
            {
                "following_id": f.following_id,
                "created_at": f.created_at
            }
            for f in following
        ])
    