# app/blog/views/toggle_post_like.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.post_like_service import toggle_like


class TogglePostLikeAPI(MethodView):

    @jwt_required()
    def post(self, post_id):

        user_id = int(get_jwt_identity())

        liked, likes = toggle_like(user_id, post_id)

        return jsonify({
            "liked": liked,
            "likes": likes
        })