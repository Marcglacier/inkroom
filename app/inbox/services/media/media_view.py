# app/inbox/services/media/media_view.py

from datetime import datetime

from app.extensions import db
from app.inbox.models.media_view import MediaView


def record_media_view(user_id: int, media_id: int):
    """
    Creates or updates a media view.
    """

    view = MediaView.query.filter_by(
        media_id=media_id,
        user_id=user_id,
    ).first()

    if view:
        view.opened_at = datetime.utcnow()
    else:
        view = MediaView(
            media_id=media_id,
            user_id=user_id,
        )
        db.session.add(view)

    db.session.commit()

    return view