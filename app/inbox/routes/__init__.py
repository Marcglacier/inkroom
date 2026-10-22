# app/inbox/routes/__init__.py

from flask import Blueprint
from .message_routes import register_message_routes
from .conversation_routes import register_conversation_routes
from .call_routes import register_call_routes
from app.inbox.api.inbox.inbox_list import InboxAPI
from app.inbox.api.inbox.get_allies import AlliesAPI
from app.inbox.api.inbox.settings.presence_settings import PresenceSettingsAPI
from app.inbox.api.inbox.settings.read_receipt_settings import (
    ReadReceiptSettingsAPI,
)
from .search_routes import search_bp
from app.inbox.api.inbox.settings.actions.restrictions import RestrictionsAPI
from app.inbox.api.inbox.settings.actions.blocks import BlocksAPI

def create_inbox_blueprint():

    inbox_bp = Blueprint( "inbox", __name__ )

    # Inbox list
    inbox_bp.add_url_rule( "", view_func=InboxAPI.as_view("inbox"), methods=["GET"] )

    # Mutual allies
    inbox_bp.add_url_rule( "/allies", view_func=AlliesAPI.as_view("allies"), methods=["GET"] )

    inbox_bp.add_url_rule( "/settings/presence", view_func=PresenceSettingsAPI.as_view("presence_settings"), methods=["GET", "PATCH"], )

    inbox_bp.add_url_rule( "/settings/read-receipts", view_func=ReadReceiptSettingsAPI.as_view( "read_receipt_settings" ), methods=["GET", "PATCH"], )

    inbox_bp.add_url_rule( "/restrictions/<int:user_id>", view_func=RestrictionsAPI.as_view("restrictions"), methods=["GET", "POST", "DELETE"], )
    inbox_bp.add_url_rule( "/blocks/<int:user_id>", view_func=BlocksAPI.as_view("blocks"), methods=["GET", "POST", "DELETE"], )
    # Messages
    register_message_routes(inbox_bp)
    # Calls
    register_call_routes(inbox_bp)
    # Conversations
    register_conversation_routes(inbox_bp)
    # Search
    inbox_bp.register_blueprint(  search_bp )

    return inbox_bp