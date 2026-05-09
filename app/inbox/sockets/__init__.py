# app/inbox/sockets/__init__.py

from app.inbox.sockets.typing_events import register_typing_events
from app.inbox.sockets.connect_events import register_connect_events


def register_socket_events(socketio):

    register_connect_events(socketio)
    register_typing_events(socketio)