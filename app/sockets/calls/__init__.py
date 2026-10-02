# app/sockets/calls/__init__.py

from .initiate import register_call_initiate
from .signaling import register_call_signaling
from .cancel import register_call_cancel
from .media import register_call_media
from .end import register_call_end
from .connection import register_call_connection

def register_call_events(socketio):
    register_call_initiate(socketio)
    register_call_signaling(socketio)
    register_call_cancel(socketio)
    register_call_media(socketio)
    register_call_end(socketio)
    register_call_connection(socketio)