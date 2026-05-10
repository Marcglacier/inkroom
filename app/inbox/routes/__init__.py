# app/inbox/routes/__init__.py
from flask import Blueprint

from app.inbox.routes.message_routes import register_message_routes
from app.inbox.routes.conversation_routes import register_conversation_routes
from app.inbox.api.inbox.inbox_list import InboxAPI


def create_inbox_blueprint():
    inbox_bp = Blueprint("inbox", __name__)

    # Inbox list
    inbox_bp.add_url_rule(
        "",
        view_func=InboxAPI.as_view("inbox"),
        methods=["GET"]
    )

    # register route groups
    register_message_routes(inbox_bp)
    register_conversation_routes(inbox_bp)

    return inbox_bp