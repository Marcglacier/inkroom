# app/sockets/calls/signaling/__init__.py
from .offer import register_call_offer
from .answer import register_call_answer
from .ice_candidate import (
    register_call_ice_candidate,
)


def register_call_signaling(socketio):
    register_call_offer(socketio)
    register_call_answer(socketio)
    register_call_ice_candidate(socketio)