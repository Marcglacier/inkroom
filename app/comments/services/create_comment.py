# app/comments/services/create_comment.py

from app.extensions import db
from app.models import Comment, Post
from app.notifications.services import NotificationService


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

    comment = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id,
        parent_id=parent_id
    )

    db.session.add(comment)
    db.session.commit()

    if not parent_id:
        if post.author_id != user_id:
            NotificationService.create_post_comment(user_id, post, comment)
    else:
        parent = Comment.query.get(parent_id)
        if parent and parent.user_id != user_id:
            NotificationService.create_comment_reply(user_id, parent, comment)

    return {"message": "Comment created", "id": comment.id}, 201