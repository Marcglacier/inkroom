from app.extensions import db
from app.models import Comment, CommentLike, Post
from .utils import build_comment_tree


def create_comment_service(data, user_id):

    content = data.get("content")
    post_id = data.get("post_id")
    parent_id = data.get("parent_id")

    if not content or not post_id:
        return {"error": "Content and post_id required"}, 400

    if not Post.query.get(post_id):
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

    return {"message": "Comment created", "id": comment.id}, 201


def toggle_like_service(comment_id, user_id):

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"error": "Comment not found"}, 404

    like = CommentLike.query.filter_by(
        user_id=user_id,
        comment_id=comment_id
    ).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return {"message": "Comment unliked"}, 200

    db.session.add(CommentLike(user_id=user_id, comment_id=comment_id))
    db.session.commit()

    return {"message": "Comment liked"}, 201


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


def delete_comment_service(comment_id, user_id):

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != int(user_id):
        return {"error": "Unauthorized"}, 403

    db.session.delete(comment)
    db.session.commit()

    return {"message": "Comment deleted"}, 200


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