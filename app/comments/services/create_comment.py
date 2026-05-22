# app/comments/services/create_comment.py
from app.extensions import db

from app.models import (
    Comment,
    Post
)

from app.notifications.services import (
    create_post_comment,
    create_comment_reply
)


def create_comment_service(data, user_id):

    content = data.get("content")
    post_id = data.get("post_id")
    parent_id = data.get("parent_id")

    if not content or not post_id:
        return {"error": "Content and post_id required"}, 400

    post = Post.query.get(post_id)

    if not post:
        return {"error": "Post not found"}, 404

    if parent_id and not Comment.query.get(parent_id):
        return {"error": "Parent comment not found"}, 404

    # =========================
    # CREATE COMMENT
    # =========================
    comment = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id,
        parent_id=parent_id
    )

    db.session.add(comment)

    # =========================
    # SAFE COUNTER UPDATE
    # =========================
    post.comments_count = (post.comments_count or 0) + 1

    db.session.commit()

    # =========================
    # NOTIFICATIONS
    # =========================
    if not parent_id:
        create_post_comment(
            actor_id=user_id,
            post=post,
            comment=comment
        )
    else:
        parent_comment = Comment.query.get(parent_id)

        if parent_comment:
            create_comment_reply(
                actor_id=user_id,
                parent_comment=parent_comment,
                reply_comment=comment
            )

    return {
        "message": "Comment created",
        "id": comment.id
    }, 201