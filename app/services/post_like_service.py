# app/services/post_like_service.py
from app.extensions import db
from app.models.post_like import PostLike
from app.models.post import Post
from app.notifications.services import NotificationService


def toggle_like(user_id, post_id):

    post = Post.query.get_or_404(post_id)

    like = PostLike.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    # =========================
    # UNLIKE FLOW
    # =========================
    if like:
        db.session.delete(like)
        post.likes_count -= 1

        db.session.commit()

        return False, post.likes_count

    # =========================
    # LIKE FLOW
    # =========================
    new_like = PostLike(
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(new_like)
    post.likes_count += 1

    db.session.commit()

    # 🔔 Notification (AFTER successful like)
    NotificationService.create_post_like(
        actor_id=user_id,
        post=post
    )

    return True, post.likes_count