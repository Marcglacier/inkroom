# app/notifications/routes.py

from flask import Blueprint

from .views.get_notifications import GetNotificationsAPI
from .views.unread_count import UnreadCountAPI
from .views.mark_as_read import MarkAsReadAPI
from .views.mark_all_as_read import MarkAllAsReadAPI

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications"
)

notifications_bp.add_url_rule(
    "",
    view_func=GetNotificationsAPI.as_view("get_notifications"),
    methods=["GET"]
)

notifications_bp.add_url_rule(
    "/unread-count",
    view_func=UnreadCountAPI.as_view("unread_count"),
    methods=["GET"]
)

notifications_bp.add_url_rule(
    "/<int:notification_id>/read",
    view_func=MarkAsReadAPI.as_view("mark_as_read"),
    methods=["PATCH"]
)

notifications_bp.add_url_rule(
    "/all/read",
    view_func=MarkAllAsReadAPI.as_view("mark_all_as_read"),
    methods=["PATCH"]
)