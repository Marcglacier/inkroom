from datetime import datetime, timedelta
from app.models.follow import Follow
from app.models.user import User
from app.storage.service import get_file_url
from app.extensions import db
from app.models.notification import Notification
from app.notifications.constants import FOLLOW_USER


def get_recent_followers(user_id, days=14):
    cutoff = datetime.utcnow() - timedelta(days=days)

    notifications = (
        Notification.query
        .filter(
            Notification.user_id == user_id,
            Notification.type == FOLLOW_USER,
            Notification.created_at >= cutoff,
        )
        .order_by(Notification.created_at.desc())
        .all()
    )

    unique = {}

    for notification in notifications:
        follower_user = db.session.get(User, notification.actor_id)
        if not follower_user:
            continue

        is_following_back = (
            Follow.query.filter_by(
                follower_id=user_id,
                following_id=follower_user.id,
            ).first()
            is not None
        )

        state = "mutual" if is_following_back else "follower"

        # Keep the most recent notification for each follower
        if follower_user.id not in unique:
            unique[follower_user.id] = {
                "id": follower_user.id,
                "username": follower_user.username,
                "name": follower_user.name,
                "avatar": (
                    get_file_url(follower_user.profile_picture)
                    if follower_user.profile_picture
                    else None
                ),
                "followed_at": notification.created_at.isoformat(),
                "state": state,
                "notification_id": notification.id,
            }

    return list(unique.values())