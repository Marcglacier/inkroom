from datetime import datetime, timedelta

from app.models.follow import Follow
from app.models.user import User


def get_recent_followers(user_id, days=14):

    cutoff = datetime.utcnow() - timedelta(days=days)

    follows = (
        Follow.query
        .filter(
            Follow.following_id == user_id,
            Follow.created_at >= cutoff
        )
        .order_by(Follow.created_at.desc())
        .all()
    )

    result = []

    for follow in follows:

        user = User.query.get(follow.follower_id)

        if not user:
            continue

        result.append({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "avatar": user.profile_picture,
            "followed_at": follow.created_at.isoformat()
        })

    return result