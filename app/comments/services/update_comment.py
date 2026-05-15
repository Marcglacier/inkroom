# app/comments/services/update_comment.py

from app.extensions import db
from app.models import Comment


def update_comment_service(comment_id, data, user_id):

    content = data.get("content")
    if not content:
        return {"error": "Content required"}, 400

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != int(user_id):
        return {"error": "Unauthorized"}, 403

    comment.content = content
    db.session.commit()

    return {
        "message": "Comment updated",
        "id": comment.id,
        "content": comment.content
    }, 200