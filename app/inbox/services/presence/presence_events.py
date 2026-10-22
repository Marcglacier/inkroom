# app/inbox/services/presence/presence_events.py
from app.extensions import db, socketio
from app.models.user import User
from app.sockets.presence_store import (
    online_users,
    last_seen,
    user_connections,
)
from app.inbox.services.settings.restriction_policy import (
    RestrictionPolicy,
)
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

def presence_payload(viewer_id, target_id):
    """Return presence only when both users allow visibility."""
    viewer = db.session.get(User, viewer_id)
    target = db.session.get(User, target_id)

    visible = (
        viewer is not None
        and target is not None
        and not viewer.is_deleted
        and not target.is_deleted
        and viewer.show_online_status
        and target.show_online_status
        and not RestrictionPolicy.restricts_either_user(
            viewer_id,
            target_id,
        )
        and not BlockPolicy.blocks_either_user(
            viewer_id,
            target_id,
        )
    )

    if not visible:
        return {
            "user_id": target_id,
            "online": False,
            "last_seen": None,
        }


    return {
        "user_id": target_id,
        "online": online_users.get(target_id, False),
        "last_seen": last_seen.get(target_id),
    }


def emit_presence_status(user_id, online, last_seen=None):
    """Send an update only to viewers allowed to see this user's presence."""
    target = db.session.get(User, user_id)
    if target is None or target.is_deleted:
        return

    for viewer_id in list(user_connections):
        payload = presence_payload(viewer_id, user_id)

        socketio.emit(
            "presence:status",
            payload,
            room=f"user_{viewer_id}",
        )

def emit_presence_snapshot(viewer_id):
    """Refresh the presence visible to one connected user."""
    if viewer_id not in user_connections:
        return

    target_ids = set(online_users) | set(user_connections)

    for target_id in target_ids:
        socketio.emit(
            "presence:status",
            presence_payload(viewer_id, target_id),
            room=f"user_{viewer_id}",
        )