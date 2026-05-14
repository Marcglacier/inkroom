# app/notifications/services/create_notification.py
from app.extensions import db
from app.models.notification import Notification


def create_notification(**kwargs):

    notif = Notification(**kwargs)

    db.session.add(notif)
    db.session.commit()

    return notif