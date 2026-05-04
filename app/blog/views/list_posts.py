# app/blog/views/list_posts.py
from flask.views import MethodView
from flask import jsonify

from app.models.post import Post


class ListPostsAPI(MethodView):

    def get(self):
        posts = Post.query.order_by(Post.created_at.desc()).all()

        data = []

        for post in posts:
            data.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author_id": post.author_id,
                "created_at": post.created_at
            })

        return jsonify(data)