# app/comments/services/delete_comment.py

from app.extensions import db
from app.models import Comment


def delete_comment_service(comment_id, user_id):

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != int(user_id):
        return {"error": "Unauthorized"}, 403

    db.session.delete(comment)
    db.session.commit()

    return {"message": "Comment deleted"}, 200