# app/notifications/services/core/group_notifications.py

from collections import defaultdict

# =========================
# TYPE NORMALIZATION MAP
# =========================
TYPE_MAP = {
    "REPOST": "REPOST_POST",
    "LIKE": "LIKE_POST",
    "COMMENT": "COMMENT_POST"
}


def group_notifications(notifications):
    grouped = {}

    for n in notifications:

        # =========================
        # NORMALIZE TYPE HERE (CRITICAL FIX)
        # =========================
        notif_type = TYPE_MAP.get(n.type, n.type)

        key = (notif_type, n.post_id, n.comment_id)

        if key not in grouped:
            grouped[key] = {
                "type": notif_type,
                "post_id": n.post_id,
                "comment_id": n.comment_id,
                "raw_notifications": [],
                "actors": [],
                "latest_created_at": n.created_at
            }

        group = grouped[key]

        group["raw_notifications"].append(n)

        if n.actor:
            group["actors"].append({
                "id": n.actor.id,
                "username": n.actor.username
            })

        if n.created_at > group["latest_created_at"]:
            group["latest_created_at"] = n.created_at

    return list(grouped.values())