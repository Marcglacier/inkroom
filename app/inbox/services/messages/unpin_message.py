# app/inbox/services/messages/unpin_message.py
from app.extensions import db
from app.inbox.models.pinned_message import PinnedMessage


def unpin_message(message_id):

    pin = PinnedMessage.query.filter_by(
        message_id=message_id
    ).first()

    if not pin:
        return {"error": "not pinned"}, 404

    db.session.delete(pin)
    db.session.commit()

    return {"message": "unpinned"}
