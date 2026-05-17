# app/comments/views/like_comment.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import CommentLike

from app.notifications.services import create_notification
from app.notifications.constants import LIKE_COMMENT


class LikeCommentAPI(MethodView):

    @jwt_required()
    def post(self, comment_id):
        user_id = int(get_jwt_identity())

        like = CommentLike.query.filter_by(
            user_id=user_id,
            comment_id=comment_id
        ).first()

        # =====================
        # UNLIKE
        # =====================
        if like:
            db.session.delete(like)
            db.session.commit()
            return jsonify({"message": "Unliked comment"})

        # =====================
        # LIKE
        # =====================
        new_like = CommentLike(
            user_id=user_id,
            comment_id=comment_id
        )

        db.session.add(new_like)
        db.session.commit()

        # =====================
        # NOTIFICATION
        # =====================
        if like is None:
            comment = new_like.comment  # assuming relationship exists

            if comment and user_id != comment.user_id:
                create_notification(
                    actor_id=user_id,
                    user_id=comment.user_id,
                    type=LIKE_COMMENT,
                    post_id=comment.post_id,
                    comment_id=comment_id
                )

        return jsonify({"message": "Comment liked"})