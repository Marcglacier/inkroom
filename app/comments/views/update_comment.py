# app/comments/views/update_comment.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Comment


class UpdateCommentAPI(MethodView):

    @jwt_required()
    def put(self, comment_id):

        user_id = get_jwt_identity()
        data = request.get_json()

        comment = Comment.query.get_or_404(comment_id)

        if comment.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        comment.content = data.get("content")

        db.session.commit()

        return jsonify({"message": "Comment updated"})