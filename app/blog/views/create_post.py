# app/blog/views/create_post.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.post import Post


class CreatePostAPI(MethodView):

    @jwt_required()
    def post(self):
        data = request.get_json()

        title = data.get("title")
        content = data.get("content")

        if not title or not content:
            return jsonify({"error": "Missing fields"}), 400

        post = Post(
            title=title,
            content=content,
            author_id=int(get_jwt_identity())
        )

        db.session.add(post)
        db.session.commit()

        return jsonify({
            "id": post.id,
            "title": post.title,
            "content": post.content
        }), 201