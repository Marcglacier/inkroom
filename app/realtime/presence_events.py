# app/realtime/presence_events.py
from flask_socketio import emit
from app.extensions import socketio
from app.realtime.registry import online_users


# =========================
# GET ONLINE USERS
# =========================
@socketio.on("get_online_users")
def handle_get_online():

    emit(
        "online_users",
        {"users": list(online_users.keys())}
    )