# app/notifications/services/create_notification.py

from app.extensions import db
from app.models.notification import Notification

# notification types that should NOT duplicate
DEDUPE_TYPES = {
    "LIKE_POST",
    "LIKE_COMMENT",
    "FOLLOW_USER",
    "FOLLOW_REQUEST"
}


def create_notification(**kwargs):

    notif_type = kwargs.get("type")

    # =====================================
    # 🔥 DEBUG: ENTRY POINT
    # =====================================
    print("\n🔥 [NOTIF DEBUG] create_notification CALLED")
    print("➡️ type:", notif_type)
    print("➡️ user_id (receiver):", kwargs.get("user_id"))
    print("➡️ actor_id:", kwargs.get("actor_id"))
    print("➡️ post_id:", kwargs.get("post_id"))
    print("➡️ comment_id:", kwargs.get("comment_id"))

    # =====================================
    # DUPLICATE PREVENTION
    # =====================================
    if notif_type in DEDUPE_TYPES:

        print("⚠️ [NOTIF DEBUG] Dedup check enabled for:", notif_type)

        existing = Notification.query.filter_by(
            user_id=kwargs.get("user_id"),
            actor_id=kwargs.get("actor_id"),
            type=notif_type,
            post_id=kwargs.get("post_id"),
            comment_id=kwargs.get("comment_id"),
            is_read=False
        ).first()

        if existing:
            print("⚠️ [NOTIF DEBUG] DUPLICATE FOUND → returning existing ID:", existing.id)
            return existing

    # =====================================
    # CREATE NEW NOTIFICATION
    # =====================================
    print("🟢 [NOTIF DEBUG] Creating new notification...")

    notif = Notification(**kwargs)

    db.session.add(notif)
    db.session.commit()

    print("✅ [NOTIF DEBUG] Saved notification ID:", notif.id)

    return notif