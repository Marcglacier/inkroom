# app/users/views/get_followers.py
from flask.views import MethodView
from flask import jsonify
from app.users.services import get_followers


class GetFollowersAPI(MethodView):

    def get(self, user_id):
        followers = get_followers(user_id)

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "name": u.name,
                "avatar_url": u.avatar_url
            }
            for u in followers
        ])