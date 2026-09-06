# app/sockets/calls/helpers/resolve_participant.py

from app.inbox.models import Call

from app.sockets.presence_store import user_connections


def get_other_participant_id(
    call: Call,
    user_id: int,
) -> int:
    if user_id == call.caller_id:
        return call.receiver_id

    return call.caller_id


def get_user_socket_ids(
    user_id: int,
) -> set[str]:
    return user_connections.get(
        user_id,
        set(),
    )