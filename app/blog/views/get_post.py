# app/blog/views/get_post.py
from flask.views import MethodView
from flask import jsonify

from app.models.post import Post


class GetPostAPI(MethodView):

    def get(self, post_id):

        post = Post.query.get_or_404(post_id)

        return jsonify({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id
        })