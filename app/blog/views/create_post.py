# app/blog/views/create_post.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.post_service import create_post


class CreatePostAPI(MethodView):

    @jwt_required()
    def post(self):

        data = request.get_json()

        post, error = create_post(
            int(get_jwt_identity()),
            data.get("title"),
            data.get("content")
        )

        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "id": post.id,
            "title": post.title,
            "content": post.content
        }), 201
    