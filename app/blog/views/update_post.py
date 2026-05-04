# app/blog/views/update_post.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.post import Post


class UpdatePostAPI(MethodView):

    @jwt_required()
    def put(self, post_id):

        post = Post.query.get_or_404(post_id)

        if post.author_id != int(get_jwt_identity()):
            return jsonify({"error": "Not authorized"}), 403

        data = request.get_json()

        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)

        db.session.commit()

        return jsonify({"message": "Post updated"})