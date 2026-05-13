# app/comments/services/get_comments.py

from app.models import Comment
from app.comments.utils import build_comment_tree


def get_comments_service(post_id):

    comments = Comment.query.filter_by(post_id=post_id).all()

    comment_list = [{
        "id": c.id,
        "content": c.content,
        "user_id": c.user_id,
        "post_id": c.post_id,
        "parent_id": c.parent_id,
        "created_at": c.created_at,
        "likes": len(c.likes)
    } for c in comments]

    return build_comment_tree(comment_list)