# app/sockets/calls/__init__.py

from .initiate import register_call_initiate
from .signaling import register_call_signaling
from .cancel import register_call_cancel

def register_call_events(socketio):
    register_call_initiate(socketio)
    register_call_signaling(socketio)
    register_call_cancel(socketio)