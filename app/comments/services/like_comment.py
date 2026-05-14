# app/comments/services/like_comment.py

from app.extensions import db

from app.models import (
    Comment,
    CommentLike
)

from app.notifications.services import (
    create_comment_like
)


def toggle_like_service(comment_id, user_id):

    comment = Comment.query.get(comment_id)

    if not comment:
        return {
            "error": "Comment not found"
        }, 404

    like = CommentLike.query.filter_by(
        user_id=user_id,
        comment_id=comment_id
    ).first()

    # =========================
    # UNLIKE
    # =========================

    if like:

        db.session.delete(like)

        db.session.commit()

        return {
            "message": "Comment unliked"
        }, 200

    # =========================
    # LIKE
    # =========================

    db.session.add(
        CommentLike(
            user_id=user_id,
            comment_id=comment_id
        )
    )

    db.session.commit()

    # =========================
    # NOTIFICATION
    # =========================

    create_comment_like(
        actor_id=user_id,
        comment=comment
    )

    return {
        "message": "Comment liked"
    }, 201