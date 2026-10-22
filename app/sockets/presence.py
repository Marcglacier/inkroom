
from flask import request
from flask_socketio import emit

from app.inbox.services.presence.presence_events import presence_payload
from app.sockets.presence_store import user_sockets


def register_presence_events(socketio):

    @socketio.on("presence:check")
    def check(data):
        viewer_id = user_sockets.get(request.sid)

        # Only authenticated sockets can check presence.
        if viewer_id is None:
            return

        try:
            target_id = int(data.get("user_id"))
        except (AttributeError, TypeError, ValueError):
            return

        emit(
            "presence:status",
            presence_payload(viewer_id, target_id),
        )
