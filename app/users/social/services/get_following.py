# app/users/social/services/get_following.py
from app.models.follow import Follow
from app.models.user import User
from app.extensions import db


def get_following(user_id):

    print(f"[FOLLOWING SERVICE] FETCHING FOLLOWING FOR USER {user_id}")

    following = (
        db.session.query(User)
        .join(
            Follow,
            Follow.following_id == User.id
        )
        .filter(
            Follow.follower_id == user_id
        )
        .all()
    )

    print(f"[FOLLOWING SERVICE] FOLLOWING COUNT: {len(following)}")

    for user in following:
        print(f"[FOLLOWING SERVICE] FOUND USER: {user.username}")

    return following