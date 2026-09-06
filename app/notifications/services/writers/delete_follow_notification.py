# app/notifications/services/writers/delete_follow_notification.py

from app.models.notification import Notification
from app.notifications.constants import FOLLOW_USER
from app.extensions import db


def delete_follow_notification(actor_id, target_user_id):
    """
    Removes the latest follow notification for this relationship.
    """

    notif = (
        Notification.query
        .filter_by(
            actor_id=actor_id,
            user_id=target_user_id,
            type=FOLLOW_USER,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    if notif:
        db.session.delete(notif)