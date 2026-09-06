from .connection import register_connection_events
from .typing import register_typing_events
from .notifications import register_notification_events
from .messaging import register_messaging_events
from .presence import register_presence_events
from .calls import register_call_events

def register_socket_events(socketio):
    register_connection_events(socketio)
    register_typing_events(socketio)
    register_notification_events(socketio)
    register_messaging_events(socketio)
    register_presence_events(socketio)
    register_call_events(socketio)