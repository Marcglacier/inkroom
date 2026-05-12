# app/inbox/routes/conversation_routes.py
from app.inbox.api.conversations.conversation_messages import ConversationMessagesAPI
from app.inbox.api.conversations.clear_conversation import ClearConversationAPI
from app.inbox.api.conversations.delete_conversation import DeleteConversationAPI
from app.inbox.api.messages.fetch_pinned_messages import FetchPinnedMessagesAPI


def register_conversation_routes(bp):

    bp.add_url_rule(
        "/conversations/<int:conversation_id>",
        view_func=ConversationMessagesAPI.as_view("conversation_messages"),
        methods=["GET"]
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/clear",
        view_func=ClearConversationAPI.as_view("clear_conversation"),
        methods=["DELETE"]
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/delete",
        view_func=DeleteConversationAPI.as_view("delete_conversation"),
        methods=["DELETE"]
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/pinned",
        view_func=FetchPinnedMessagesAPI.as_view("fetch_pinned"),
        methods=["GET"]
    )