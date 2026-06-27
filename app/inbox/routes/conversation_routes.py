# app/inbox/routes/conversation_routes.py
from app.inbox.api.conversations.conversation_messages import ConversationMessagesAPI
from app.inbox.api.conversations.clear_conversation import ClearConversationAPI
from app.inbox.api.conversations.delete_conversation import DeleteConversationAPI
from app.inbox.api.messages.fetch_pinned_messages import FetchPinnedMessagesAPI
from app.inbox.api.conversations.start_conversation import StartConversationAPI
from app.inbox.api.conversations.conversation_detail import ConversationDetailAPI
from app.inbox.api.conversations.get_request_conversation import RequestConversationAPI
from app.inbox.api.conversations.accept_request import AcceptRequestAPI
from app.inbox.api.conversations.reject_request import RejectRequestAPI
from app.inbox.api.conversations.list_requests import ListRequestsAPI
from app.inbox.api.conversations.restore_request import RestoreRequestAPI

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

    bp.add_url_rule(
        "/conversations/start/<int:user_id>",
        view_func=StartConversationAPI.as_view(
        "start_conversation"
        ),
        methods=["POST"]
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/detail",
        view_func=ConversationDetailAPI.as_view(
            "conversation_detail"
        ),
        methods=["GET"]
    )

    bp.add_url_rule(
        "/requests/<int:conversation_id>",
        view_func=RequestConversationAPI.as_view(
            "request_conversation"
        )
    )

    bp.add_url_rule(
        "/requests/<int:conversation_id>/accept",
        view_func=AcceptRequestAPI.as_view(
            "accept_request"
        )
    )

    bp.add_url_rule(
         "/requests/<int:conversation_id>/reject",
         view_func=RejectRequestAPI.as_view(
            "reject_request"
         )
    )

    bp.add_url_rule(
        "/requests",
        view_func=ListRequestsAPI.as_view(
        "list_requests"),
        methods=["GET"]
    )

    bp.add_url_rule(
    "/requests/<int:conversation_id>/restore",
    view_func=RestoreRequestAPI.as_view(
        "restore_request"
    )
)

