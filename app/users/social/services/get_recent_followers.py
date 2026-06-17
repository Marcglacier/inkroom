from datetime import datetime, timedelta
from app.models.follow import Follow
from app.models.user import User
from app.models.profile import Profile


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

        follower_user = User.query.get(follow.follower_id)
        if not follower_user:
            continue

        profile = Profile.query.filter_by(user_id=follower_user.id).first()

        # 🔥 FIX: check if current user follows them back
        is_following_back = Follow.query.filter_by(
            follower_id=user_id,
            following_id=follower_user.id
        ).first() is not None

        result.append({
            "id": follower_user.id,
            "username": follower_user.username,
            "name": follower_user.name,
            "avatar": profile.avatar_url if profile else None,
            "followed_at": follow.created_at.isoformat(),
            "is_following_back": is_following_back
        })

    return result