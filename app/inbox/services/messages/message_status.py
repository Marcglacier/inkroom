from app.sockets.presence_store import online_users
from app.sockets.messaging import active_chambers


def get_message_status(
    receiver_id,
    conversation_id,
    conversation_status=None,
):
    online = online_users.get(receiver_id, False)
    in_chat = (
        active_chambers.get(receiver_id)
        == conversation_id
    )

    if conversation_status == "pending":
        status = "pending_request"
    elif in_chat:
        status = "read"
    elif online:
        status = "delivered"
    else:
        status = "sent"

    return status, online, in_chat