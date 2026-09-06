# app/notifications/services/__init__.py

from .writers.create_notification import (
    notification_creator, create_notification,
)

# =========================
# WRITERS (CREATE EVENTS)
# =========================

from .writers.create_post_like import create_post_like
from .writers.create_post_comment import create_post_comment
from .writers.create_comment_like import create_comment_like
from .writers.create_comment_reply import create_comment_reply
from .writers.create_follow_notification import (
    create_follow_notification,
)
from .writers.create_follow_accept_notification import (
    create_follow_accept_notification,
)
from .writers.create_follow_request_notification import (
    create_follow_request_notification,
)
from .writers.create_post_repost import create_post_repost

# =========================
# READERS (FETCH DATA)
# =========================

from .readers.get_notifications import get_notifications

# =========================
# CORE (BUSINESS LOGIC)
# =========================

from .core.group_notifications import group_notifications
from .core.message_builder import build_notification_message

# =========================
# ACTIONS (STATE CHANGES)
# =========================

from .actions.mark_as_read import mark_as_read
from .actions.mark_all_as_read import mark_all_as_read


__all__ = [
    # Creator
    "notification_creator",
    "create_notification",

    # Writers
    "create_post_like",
    "create_post_comment",
    "create_comment_like",
    "create_comment_reply",
    "create_follow_notification",
    "create_follow_accept_notification",
    "create_follow_request_notification",
    "create_post_repost",

    # Readers
    "get_notifications",

    # Core
    "group_notifications",
    "build_notification_message",

    # Actions
    "mark_as_read",
    "mark_all_as_read",
]