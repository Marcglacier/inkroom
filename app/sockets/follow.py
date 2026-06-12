# app/sockets/follow.py

from app.users.social.services.relationship_service import (
    get_relationship
)
from app.users.social.services.follow_counts import (
    get_follow_counts
)
from app.extensions import socketio


def emit_relationship_update(viewer_id, target_id):

    print("\n")
    print("🔥 RELATIONSHIP UPDATE CALLED")
    print("viewer:", viewer_id)
    print("target:", target_id)

    relationship = get_relationship(
        viewer_id,
        target_id
    )

    counts = get_follow_counts(target_id)

    payload = {
        "viewerId": viewer_id,
        "targetId": target_id,
        **relationship,
        **counts,
    }

    print("📦 PAYLOAD:")
    print(payload)

    print(f"📡 EMIT -> user_{viewer_id}")

    socketio.emit(
        "relationship:update",
        payload,
        room=f"user_{viewer_id}",
    )

    print(f"📡 EMIT -> user_{target_id}")

    socketio.emit(
        "relationship:update",
        payload,
        room=f"user_{target_id}",
    )

    print("✅ RELATIONSHIP UPDATE SENT")
    print("\n")