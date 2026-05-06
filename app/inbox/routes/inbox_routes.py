# app/inbox/routes/inbox_routes.py
from flask import Blueprint

from app.inbox.views.send_message import SendMessageAPI
from app.inbox.views.inbox_list import InboxAPI
from app.inbox.views.conversation_messages import ConversationMessagesAPI
from app.inbox.views.edit_message import EditMessageAPI
from app.inbox.views.delete_message import DeleteMessageAPI
from app.inbox.views.undo_delete import UndoDeleteAPI

inbox_bp = Blueprint("inbox", __name__)

# GET /api/inbox
inbox_bp.add_url_rule(
    "",
    view_func=InboxAPI.as_view("inbox"),
    methods=["GET"]
)

# POST /api/inbox/messages/<user_id>
inbox_bp.add_url_rule(
    "/messages/<int:user_id>",
    view_func=SendMessageAPI.as_view("send_message"),
    methods=["POST"]
)

# GET /api/inbox/conversations/<conversation_id>
inbox_bp.add_url_rule(
    "/conversations/<int:conversation_id>",
    view_func=ConversationMessagesAPI.as_view("conversation_messages"),
    methods=["GET"]
)

# PUT /api/inbox/messages/<message_id>
inbox_bp.add_url_rule(
    "/messages/<int:message_id>",
    view_func=EditMessageAPI.as_view("edit_message"),
    methods=["PUT"]
)

# DELETE /api/inbox/messages/<message_id>
inbox_bp.add_url_rule(
    "/messages/<int:message_id>",
    view_func=DeleteMessageAPI.as_view("delete_message"),
    methods=["DELETE"]
)

# POST /api/inbox/messages/<message_id>/undo_delete
inbox_bp.add_url_rule(
    "/messages/<int:message_id>/undo_delete",
    view_func=UndoDeleteAPI.as_view("undo_delete"),
    methods=["POST"]
)