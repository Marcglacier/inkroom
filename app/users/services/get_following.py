# app/users/services/get_following.py

from app.models.follow import Follow
from app.models.user import User
from app.extensions import db


def get_following(user_id):
    return (
        db.session.query(User)
        .join(Follow, Follow.following_id == User.id)
        .filter(
            Follow.follower_id == user_id,
            Follow.accepted.is_(True)
        )
        .all()
    )