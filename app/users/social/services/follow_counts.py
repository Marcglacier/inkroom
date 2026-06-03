from app.models.follow import Follow


def get_follow_counts(user_id):
    followers = Follow.query.filter_by(
        following_id=user_id,
        status="following"
    ).count()

    following = Follow.query.filter_by(
        follower_id=user_id,
        status="following"
    ).count()

    return {
        "followers_count": followers,
        "following_count": following
    }