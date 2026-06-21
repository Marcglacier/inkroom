from flask import Blueprint

from app.inbox.api.inbox.inbox_list import InboxAPI
from app.inbox.routes.message_routes import register_message_routes
from app.inbox.routes.conversation_routes import register_conversation_routes


inbox_bp = Blueprint("inbox", __name__)

# inbox list
inbox_bp.add_url_rule(
    "",
    view_func=InboxAPI.as_view("inbox"),
    methods=["GET"]
)

# register subroutes
register_message_routes(inbox_bp)
register_conversation_routes(inbox_bp)