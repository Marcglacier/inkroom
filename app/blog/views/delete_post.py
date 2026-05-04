# app/blog/views/delete_post.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.post_service import delete_post


class DeletePostAPI(MethodView):

    @jwt_required()
    def delete(self, post_id):

        success, error, status = delete_post(
            post_id,
            int(get_jwt_identity())
        )

        if error:
            return jsonify({"error": error}), status

        return jsonify({"message": "Post deleted"})