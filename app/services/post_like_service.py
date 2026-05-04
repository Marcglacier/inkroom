# app/services/post_like_service.py
from app.extensions import db
from app.models.post_like import PostLike
from app.models.post import Post


def toggle_like(user_id, post_id):

    post = Post.query.get_or_404(post_id)

    like = PostLike.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if like:
        db.session.delete(like)
        post.likes_count -= 1
        db.session.commit()
        return False, post.likes_count

    new_like = PostLike(
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(new_like)
    post.likes_count += 1

    db.session.commit()

    return True, post.likes_count