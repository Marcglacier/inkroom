from app.models.notification import Notification
from app.models.profile import Profile


def get_notifications(user_id):

    notifications = (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    result = []

    for n in notifications:

        profile = None

        if n.actor:
            profile = Profile.query.filter_by(
                user_id=n.actor.id
            ).first()

        result.append({
            "id": n.id,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": n.created_at,

            "actor": {
                "id": n.actor.id if n.actor else None,
                "username": n.actor.username if n.actor else None,
                "name": n.actor.name if n.actor else None,
                "avatar": profile.avatar_url if profile else None,
            } if n.actor else None,

            "extra": {
                "post_id": getattr(n, "post_id", None),
                "comment_id": getattr(n, "comment_id", None),
            }
        })

    return result