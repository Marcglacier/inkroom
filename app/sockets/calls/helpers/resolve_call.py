# app/sockets/calls/helpers/resolve_call.py

from app.inbox.models import Call


def resolve_call(call_id: int) -> Call | None:
    return Call.query.get(call_id)