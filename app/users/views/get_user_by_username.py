# app/users/views/get_user_by_username.py

from flask.views import MethodView
from flask import jsonify

from app.models.user import User
from app.models.profile import Profile


class GetUserByUsernameAPI(MethodView):

    def get(self, username):
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        profile = Profile.query.filter_by(user_id=user.id).first()

        return jsonify({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "avatar_url": profile.avatar_url if profile else None,
        })