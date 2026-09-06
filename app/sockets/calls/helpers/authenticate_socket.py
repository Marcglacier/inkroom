# app/sockets/calls/helpers/authenticate_socket.py

from flask import request

from app.sockets.presence_store import user_sockets


def get_authenticated_socket_user() -> int | None:
    return user_sockets.get(request.sid)