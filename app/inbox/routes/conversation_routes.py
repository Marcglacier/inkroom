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
from app.inbox.api.inbox.open_media import OpenMediaAPI
from app.inbox.api.inbox.get_media import GetArchiveMediaAPI
from app.inbox.api.conversations.mark_conversation_read import MarkConversationReadAPI
from app.inbox.api.conversations.MessageContext import MessageContextAPI
from app.inbox.api.archive.archive_conversation_api import  ArchiveConversationAPI
from app.inbox.api.archive.get_archived_conversations_api import ( GetArchivedConversationsAPI, )
from app.inbox.api.archive.restore_conversation_api import RestoreConversationAPI
from app.inbox.api.conversations.pins.pin_conversation_api import PinConversationAPI
from app.inbox.api.conversations.pins.unpin_conversation_api import UnpinConversationAPI
from app.inbox.api.conversations.mutes.mute_conversation_api import (
    MuteConversationAPI,
)

from app.inbox.api.conversations.mutes.unmute_conversation_api import (
    UnmuteConversationAPI,
)
from app.inbox.api.inbox.get_archive_links import GetArchiveLinksAPI
from app.inbox.api.inbox.open_link import OpenLinkAPI

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
        "restore_request")
    )

    bp.add_url_rule(
        "/media/<int:media_id>/open",
        view_func=OpenMediaAPI.as_view("open_media"),
        methods=["POST"]
    )
    bp.add_url_rule(
    "/links/<int:link_id>/open",
        view_func=OpenLinkAPI.as_view("open_link"),
        methods=["POST"],
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/archive",
        view_func=GetArchiveMediaAPI.as_view("get_archive_media"),
        methods=["GET"]
    )
    bp.add_url_rule(
        "/conversations/<int:conversation_id>/archive/links",
        view_func=GetArchiveLinksAPI.as_view("get_archive_links"),
        methods=["GET"]
    )

    bp.add_url_rule( "/conversations/<int:conversation_id>/read", 
        view_func=MarkConversationReadAPI.as_view("mark_conversation_read"),
         methods=["POST"],)

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/messages/<int:message_id>/context",
        view_func=MessageContextAPI.as_view("message_context"),
        methods=["GET"]
        )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/archive", 
        view_func=ArchiveConversationAPI.as_view("archive_conversation"),
        methods=["POST"]            
    )    

    bp.add_url_rule(
        "/archive",
        view_func=GetArchivedConversationsAPI.as_view( "get_archived_conversations" ),
        methods=["GET"]
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/archive",
        view_func=RestoreConversationAPI.as_view( "restore_conversation", ),
        methods=["DELETE"],
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/pin",
        view_func=PinConversationAPI.as_view( "pin_conversation", ),
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/pin",
        view_func=UnpinConversationAPI.as_view( "unpin_conversation", ),
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/mute",
        view_func=MuteConversationAPI.as_view(
            "mute_conversation",
        ),
    )

    bp.add_url_rule(
        "/conversations/<int:conversation_id>/mute",
        view_func=UnmuteConversationAPI.as_view(
            "unmute_conversation",
        ),
    )