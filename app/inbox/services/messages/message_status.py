from app.sockets.presence_store import online_users


def get_message_status(
    receiver_id,
    conversation_status=None,
):
    online = online_users.get(receiver_id, False)

    if conversation_status == "pending":
        status = "pending_request"
    elif online:
        status = "delivered"
    else:
        status = "sent"

    return status, online