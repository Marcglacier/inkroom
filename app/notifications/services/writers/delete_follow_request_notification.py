# app/notifications/services/writers/delete_follow_request_notification.py

from app.extensions import db
from app.models.notification import Notification
from app.notifications.constants import FOLLOW_REQUEST


def delete_follow_request_notification(actor_id, target_user_id):
    """
    Removes the latest follow request notification for this relationship.
    """

    notif = (
        Notification.query
        .filter_by(
            actor_id=actor_id,
            user_id=target_user_id,
            type=FOLLOW_REQUEST,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    if notif:
        db.session.delete(notif)
        db.session.commit()