# app/inbox/routes/call_routes.py

from app.inbox.api.calls.start_call import StartCallAPI
from app.inbox.api.calls.accept_call import AcceptCallAPI
from app.inbox.api.calls.decline_call import DeclineCallAPI
from app.inbox.api.calls.cancel_call import CancelCallAPI
from app.inbox.api.calls.end_call import EndCallAPI


def register_call_routes(inbox_bp):

    inbox_bp.add_url_rule(
        "/calls",
        view_func=StartCallAPI.as_view("start_call"),
        methods=["POST"],
    )

    inbox_bp.add_url_rule(
        "/calls/<int:call_id>/accept",
        view_func=AcceptCallAPI.as_view("accept_call"),
        methods=["POST"],
    )

    inbox_bp.add_url_rule(
        "/calls/<int:call_id>/decline",
        view_func=DeclineCallAPI.as_view("decline_call"),
        methods=["POST"],
    )

    inbox_bp.add_url_rule(
        "/calls/<int:call_id>/cancel",
        view_func=CancelCallAPI.as_view("cancel_call"),
        methods=["POST"],
    )

    inbox_bp.add_url_rule(
        "/calls/<int:call_id>/end",
        view_func=EndCallAPI.as_view("end_call"),
        methods=["POST"],
    )