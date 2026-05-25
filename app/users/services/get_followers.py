# app/users/services/get_followers.py

from app.models.follow import Follow
from app.models.user import User
from app.extensions import db


def get_followers(user_id):
    return (
        db.session.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(
            Follow.following_id == user_id,
            Follow.status == "accepted"
        )
        .all()
    )