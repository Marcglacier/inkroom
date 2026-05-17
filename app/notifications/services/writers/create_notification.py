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
    # GROUP / DEDUPE CHECK
    # =====================================
    if notif_type in DEDUPE_TYPES:

        print("⚠️ [NOTIF DEBUG] Dedup/grouping enabled for:", notif_type)

        existing = Notification.query.filter_by(
            user_id=kwargs.get("user_id"),
            type=notif_type,
            post_id=kwargs.get("post_id"),
            comment_id=kwargs.get("comment_id"),
            is_read=False
        ).first()

        # =====================================
        # UPDATE EXISTING GROUP
        # =====================================
        if existing:

            print("⚠️ [NOTIF DEBUG] EXISTING GROUP FOUND")
            print("➡️ Existing ID:", existing.id)

            actors = []

            # safe read of existing grouping data
            if existing.extra and isinstance(existing.extra, dict):
                actors = existing.extra.get("actors", [])

            print("➡️ Previous actors:", actors)

            new_actor = kwargs.get("actor_id")

            if new_actor not in actors:
                actors.append(new_actor)
                print("🟡 [NOTIF DEBUG] Added new actor:", new_actor)
            else:
                print("ℹ️ [NOTIF DEBUG] Actor already in group")

            existing.extra = existing.extra or {}
            existing.extra["actors"] = actors

            db.session.commit()

            print("✅ [NOTIF DEBUG] Updated grouped notification:", existing.id)
            return existing

    # =====================================
    # CREATE NEW NOTIFICATION
    # =====================================
    print("🟢 [NOTIF DEBUG] Creating new notification...")

    notif = Notification(**kwargs)

    notif.extra = {
        "actors": [kwargs.get("actor_id")]
    }

    db.session.add(notif)
    db.session.commit()

    print("✅ [NOTIF DEBUG] Saved notification ID:", notif.id)
    print("➡️ Initial actors:", notif.extra["actors"])

    return notif