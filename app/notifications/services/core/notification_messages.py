# app/notifications/services/core/notification_messages.py

from app.notifications.constants import (
    LIKE_POST,
    COMMENT_POST,
    REPOST_POST,
    FOLLOW_USER,
    REPLY_COMMENT,
    LIKE_COMMENT
)


def build_notification_message(group):

    actors = group["actors"]
    notif_type = group["type"]

    count = len(actors)

    # =========================
    # NAME FORMATTING
    # =========================
    if count == 1:
        name_part = actors[0]["username"]

    elif count == 2:
        name_part = (
            f"{actors[0]['username']} "
            f"and {actors[1]['username']}"
        )

    else:
        names = [a["username"] for a in actors[:3]]
        remaining = count - 3

        name_part = ", ".join(names)

        if remaining > 0:
            name_part += f" and {remaining} others"

    # =========================
    # ACTION MAPPING
    # =========================
    message_map = {
        LIKE_POST: "liked your post",
        COMMENT_POST: "commented on your post",
        REPOST_POST: "reposted your post",
        FOLLOW_USER: "started following you",
        REPLY_COMMENT: "replied to your comment",
        LIKE_COMMENT: "liked your comment"
    }

    action = message_map.get(
        notif_type,
        "interacted with you"
    )

    return f"{name_part} {action}"