# app/users/views/get_followers.py
from flask.views import MethodView
from flask import jsonify
from app.users.services import get_following


class GetFollowingAPI(MethodView):

    def get(self, user_id):
        following = get_following(user_id)

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "name": u.name,
                "avatar_url": u.avatar_url
            }
            for u in following
        ])