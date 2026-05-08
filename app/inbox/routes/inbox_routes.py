# app/inbox/routes/inbox_routes.py
from flask import Blueprint

from app.inbox.views.send_message import SendMessageAPI
from app.inbox.views.inbox_list import InboxAPI
from app.inbox.views.conversation_messages import ConversationMessagesAPI
from app.inbox.views.edit_message import EditMessageAPI
from app.inbox.views.delete_message import DeleteMessageAPI
from app.inbox.views.undo_delete import UndoDeleteAPI
from app.inbox.views.clear_conversation import ClearConversationAPI
from app.inbox.views.delete_conversation import DeleteConversationAPI
from app.inbox.views.react_to_message import ReactToMessageAPI

inbox_bp = Blueprint("inbox", __name__)
clear_conversation_view = ClearConversationAPI.as_view("clear_conversation")

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

# DELETE /api/inbox/conversations/<conversation_id>/clear
inbox_bp.add_url_rule(
    "/conversations/<int:conversation_id>/clear",
    view_func=clear_conversation_view,
    methods=["DELETE"]
)

# DELETE /api/inbox/conversations/<conversation_id>/delete
inbox_bp.add_url_rule(
    "/conversations/<int:conversation_id>/delete",
    view_func=DeleteConversationAPI.as_view("delete_conversation"),
    methods=["DELETE"]
)

# POST /api/inbox/messages/<message_id>/react
inbox_bp.add_url_rule(
    "/messages/<int:message_id>/react",
    view_func=ReactToMessageAPI.as_view("react_to_message"),
    methods=["POST"]
)