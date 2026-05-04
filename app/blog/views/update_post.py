# app/blog/views/update_post.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.post_service import update_post


class UpdatePostAPI(MethodView):

    @jwt_required()
    def put(self, post_id):

        data = request.get_json()

        post, error, status = update_post(
            post_id,
            int(get_jwt_identity()),
            data.get("title"),
            data.get("content")
        )

        if error:
            return jsonify({"error": error}), status

        return jsonify({"message": "Post updated"})