# app/inbox/routes/search_routes.py

from flask import Blueprint
from app.inbox.api.search.search_inbox_api import SearchInboxAPI
from app.inbox.api.search.search_conversation_api import SearchConversationAPI

search_bp = Blueprint("inbox_search", __name__)

search_inbox_view = SearchInboxAPI.as_view("search_inbox_api")
search_conversation_view = SearchConversationAPI.as_view("search_conversation_api")


search_bp.add_url_rule(
    "/search",
    view_func=search_inbox_view,
    methods=["GET"]
)

search_bp.add_url_rule(
    "/conversations/<int:conversation_id>/search",
    view_func=search_conversation_view,
    methods=["GET"]
)