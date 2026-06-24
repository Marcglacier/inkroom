from flask_socketio import emit
from app.sockets.presence_store import (
    online_users,
    last_seen
)



def register_presence_events(socketio):


    @socketio.on(
        "presence:check"
    )
    def check(data):

        user_id = int(
            data["user_id"]
        )


        emit(
            "presence:status",
            {
                "user_id": user_id,

                "online":
                    online_users.get(
                        user_id,
                        False
                    ),

                "last_seen":
                    last_seen.get(
                        user_id
                    )
            }
        )