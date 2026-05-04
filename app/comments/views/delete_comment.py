# app/comments/views/delete_comment.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Comment


class DeleteCommentAPI(MethodView):

    @jwt_required()
    def delete(self, comment_id):

        user_id = get_jwt_identity()

        comment = Comment.query.get_or_404(comment_id)

        if comment.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.delete(comment)
        db.session.commit()

        return jsonify({"message": "Comment deleted"})