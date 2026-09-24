# app/sockets/calls/helpers/build_call_payload.py

from app.inbox.models import Call
from app.inbox.serializers.call_serializer import CallSerializer
from app.models.user import User
from app.storage.service import get_file_url


def build_call_payload(
    call: Call,
    caller: User,
) -> dict:
    return {
        "call": CallSerializer(
            call
        ).to_dict(),

        "caller": {
            "id": caller.id,
            "username": caller.username,
            "name": caller.name,
            "avatar": (
                get_file_url(caller.profile_picture)
                if caller.profile_picture
                else None
            ),
        },
    }