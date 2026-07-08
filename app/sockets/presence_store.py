from datetime import datetime, timezone
import threading
from app.inbox.services.presence.presence_events import (
    emit_presence_status
)

online_users: dict[int, bool] = {}
last_seen: dict[int, str] = {}

user_sockets: dict[str, int] = {}          # sid -> user_id
user_connections: dict[int, set[str]] = {} # user_id -> set(sid)
disconnect_timers: dict[str, threading.Timer] = {} # sid -> timer


def set_online(user_id: int, sid: str) -> None:
    """Mark a user online and register their socket ID."""
    online_users[user_id] = True
    user_sockets[sid] = user_id
    user_connections.setdefault(user_id, set()).add(sid)

    # Cancel ALL pending disconnect timers for this user
    for socket_id in list(user_connections[user_id]):
        timer = disconnect_timers.pop(socket_id, None)
        if timer:
            timer.cancel()
            print(f"🛑 CANCELLED TIMER FOR {socket_id}")

    print(f"🟢 ONLINE {user_id} | SOCKETS {user_connections[user_id]}")

def remove_socket(sid: str) -> int | None:
    """Remove a socket and return user_id if fully disconnected."""
    user_id = user_sockets.pop(sid, None)
    if not user_id:
        return None

    sockets = user_connections.get(user_id, set())
    sockets.discard(sid)

    print(f"❌ REMOVED {sid} USER {user_id} LEFT {sockets}")

    if sockets:
        print("🟢 STILL ONLINE")
        return None

    user_connections.pop(user_id, None)
    return user_id


def set_offline_later(sid: str, callback, delay: int = 20) -> None:
    """Schedule a user to go offline after delay if no sockets remain."""

    def go_offline():
        # If this timer was cancelled, don't do anything
        if sid not in disconnect_timers:
            print(f"⏭ TIMER CANCELLED FOR {sid}")
            return

        # Remove this timer from the registry
        disconnect_timers.pop(sid, None)

        user_id = remove_socket(sid)
        if not user_id:
            return

        online_users[user_id] = False
        last_seen[user_id] = datetime.now(timezone.utc).isoformat()

        print(f"🔴 OFFLINE {user_id}")
        callback(user_id)

    timer = threading.Timer(delay, go_offline)
    disconnect_timers[sid] = timer
    timer.start()