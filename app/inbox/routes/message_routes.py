# app/inbox/routes/message_routes.py
from app.inbox.api.messages.send_message import SendMessageAPI
from app.inbox.api.messages.edit_message import EditMessageAPI
from app.inbox.api.messages.delete_message import DeleteMessageAPI
from app.inbox.api.messages.undo_delete import UndoDeleteAPI
from app.inbox.api.messages.react_to_message import ReactToMessageAPI
from app.inbox.api.messages.forward_message import ForwardMessageAPI
from app.inbox.api.messages.pin_message import PinMessageAPI
from app.inbox.api.messages.unpin_message import UnpinMessageAPI

def register_message_routes(bp):

    bp.add_url_rule(
        "/messages/<int:user_id>",
        view_func=SendMessageAPI.as_view("send_message"),
        methods=["POST"]
    )

    bp.add_url_rule(
        "/messages/<int:message_id>",
        view_func=EditMessageAPI.as_view("edit_message"),
        methods=["PUT"]
    )

    bp.add_url_rule(
        "/messages/<int:message_id>",
        view_func=DeleteMessageAPI.as_view("delete_message"),
        methods=["DELETE"]
    )

    bp.add_url_rule(
        "/messages/<int:message_id>/undo_delete",
        view_func=UndoDeleteAPI.as_view("undo_delete"),
        methods=["POST"]
    )

    bp.add_url_rule(
        "/messages/<int:message_id>/react",
        view_func=ReactToMessageAPI.as_view("react_to_message"),
        methods=["POST"]
    )

    bp.add_url_rule(
        "/messages/forward",
        view_func=ForwardMessageAPI.as_view("forward_message"),
        methods=["POST"]
    )

    bp.add_url_rule(
        "/messages/<int:message_id>/pin",
        view_func=PinMessageAPI.as_view("pin_message"),
        methods=["POST"]
    )

    bp.add_url_rule(
        "/messages/<int:message_id>/pin",
        view_func=UnpinMessageAPI.as_view("unpin_message"),
        methods=["DELETE"]
    )


