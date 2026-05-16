# app/feed/views/following_feed.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.follow import Follow
from app.models.post import Post
from app.models.repost import Repost


class FollowingFeedAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        # STEP 1: get people I follow
        following_ids = [
            f.following_id
            for f in Follow.query.filter_by(follower_id=user_id)
        ]

        # include my own posts
        following_ids.append(user_id)

        # STEP 2: query posts
        posts_query = Post.query.filter(
            Post.author_id.in_(following_ids)
        ).order_by(Post.created_at.desc())

        posts = posts_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # STEP 3: format response
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

              # 🚀 FAST CACHED COUNTERS (NO QUERIES)
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