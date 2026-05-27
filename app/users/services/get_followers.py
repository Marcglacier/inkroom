from app.models.follow import Follow
from app.models.user import User
from app.extensions import db


def get_followers(user_id):

    print(f"[FOLLOWERS SERVICE] FETCHING FOLLOWERS FOR USER {user_id}")

    followers = (
        db.session.query(User)
        .join(
            Follow,
            Follow.follower_id == User.id
        )
        .filter(
            Follow.following_id == user_id
        )
        .all()
    )

    print(f"[FOLLOWERS SERVICE] FOLLOWERS COUNT: {len(followers)}")

    for user in followers:
        print(f"[FOLLOWERS SERVICE] FOUND USER: {user.username}")

    return followers