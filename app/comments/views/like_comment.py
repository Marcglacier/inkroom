# app/comments/views/like_comment.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import CommentLike


class LikeCommentAPI(MethodView):

    @jwt_required()
    def post(self, comment_id):
        user_id = get_jwt_identity()

        like = CommentLike.query.filter_by(
            user_id=user_id,
            comment_id=comment_id
        ).first()

        if like:
            db.session.delete(like)
            db.session.commit()
            return jsonify({"message": "Unliked comment"})

        new_like = CommentLike(
            user_id=user_id,
            comment_id=comment_id
        )

        db.session.add(new_like)
        db.session.commit()

        return jsonify({"message": "Comment liked"})