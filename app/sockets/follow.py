# app/sockets/follow.py

from app.users.social.services.relationship_service import (
    get_relationship,
)
from app.users.social.services.follow_counts import (
    get_follow_counts,
)
from app.extensions import socketio


def emit_relationship_updates(viewer_id, target_id):

    print("\n")
    print("🔥 RELATIONSHIP UPDATE CALLED")
    print("viewer:", viewer_id)
    print("target:", target_id)

    # Relationship: viewer → target
    viewer_relationship = get_relationship(
        viewer_id,
        target_id,
    )

    # Relationship: target → viewer
    target_relationship = get_relationship(
        target_id,
        viewer_id,
    )

    # Counts for BOTH users
    viewer_counts = get_follow_counts(viewer_id)
    target_counts = get_follow_counts(target_id)

    # Payload for the user who acted
    # This relationship is:
    # viewer → target
    # Counts describe the TARGET profile
    viewer_payload = {
        "viewerId": viewer_id,
        "targetId": target_id,
        **viewer_relationship,

        "target_followers_count":
            target_counts["followers_count"],

        "target_following_count":
            target_counts["following_count"],
    }

    # Payload for the other user
    # This relationship is:
    # target → viewer
    # Counts describe the VIEWER profile
    target_payload = {
        "viewerId": target_id,
        "targetId": viewer_id,
        **target_relationship,

        "target_followers_count":
            viewer_counts["followers_count"],

        "target_following_count":
            viewer_counts["following_count"],
    }

    print("📦 VIEWER PAYLOAD")
    print(viewer_payload)

    print("📦 TARGET PAYLOAD")
    print(target_payload)

    # Send to viewer
    socketio.emit(
        "relationship:update",
        viewer_payload,
        room=f"user_{viewer_id}",
    )

    # Send to target
    socketio.emit(
        "relationship:update",
        target_payload,
        room=f"user_{target_id}",
    )

    print("✅ RELATIONSHIP UPDATE SENT\n")