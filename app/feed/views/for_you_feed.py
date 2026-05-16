# app/feed/views/for_you_feed.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.models.post import Post


class ForYouFeedAPI(MethodView):

    @jwt_required()
    def get(self):

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        posts = Post.query.order_by(
            Post.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        data = []

        for post in posts.items:
            data.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,

                "author": {
                    "id": post.author.id,
                    "username": post.author.username
                },

                # 🚀 cached counters (NO .count())
                "likes_count": post.likes_count,
                "comments_count": post.comments_count,
                "reposts_count": post.reposts_count
            })

        return jsonify({
            "page": page,
            "per_page": per_page,
            "total": posts.total,
            "posts": data
        })