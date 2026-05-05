# app/services/follow_service.py
from app.extensions import db
from app.models.follow import Follow
from app.models.user import User


def follow_user(follower_id, following_id):

    if follower_id == following_id:
        raise ValueError("Users cannot follow themselves")

    user = User.query.get_or_404(following_id)

    existing = Follow.query.filter_by(
        follower_id=follower_id,
        following_id=following_id
    ).first()

    if existing:
        return {"following": True}

    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )

    db.session.add(follow)
    db.session.commit()

    return {"following": True}


def unfollow_user(follower_id, following_id):

    follow = Follow.query.filter_by(
        follower_id=follower_id,
        following_id=following_id
    ).first()

    if not follow:
        return {"following": False}

    db.session.delete(follow)
    db.session.commit()

    return {"following": False}


def get_followers(user_id):

    followers = Follow.query.filter_by(
        following_id=user_id
    ).all()

    return [f.follower_id for f in followers]


def get_following(user_id):

    following = Follow.query.filter_by(
        follower_id=user_id
    ).all()

    return [f.following_id for f in following]