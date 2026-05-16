# app/blog/views/toggle_post_like.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.post_like_service import toggle_like
from app.notifications.services import create_notification
from app.models.post import Post

class TogglePostLikeAPI(MethodView):

    @jwt_required()
    def post(self, post_id):

        user_id = int(get_jwt_identity())

        liked, likes = toggle_like(user_id, post_id)
        post = Post.query.get(post_id)
        if liked:
            # NOTIFY POST AUTHOR
            if user_id != post.author_id:
                create_notification(
                    actor_id=user_id,
                    user_id=post.author_id,
                    type="LIKE",
                    post_id=post.id
                )


        return jsonify({
            "liked": liked,
            "likes": likes
        })