from datetime import datetime, timezone
import threading


online_users = {}

last_seen = {}

# sid -> user
user_sockets = {}

# user -> many sockets
user_connections = {}

disconnect_timers = {}



def set_online(user_id, sid):


    online_users[user_id] = True


    user_sockets[sid] = user_id


    if user_id not in user_connections:

        user_connections[user_id] = set()


    user_connections[user_id].add(sid)



    timer = disconnect_timers.pop(user_id,None)


    if timer:

        timer.cancel()



    print(
        "🟢 ONLINE",
        user_id
    )


    print(
        "SOCKET COUNT",
        len(user_connections[user_id])
    )





def set_offline_later(
    sid,
    callback,
    delay=20
):


    user_id = user_sockets.get(sid)


    if not user_id:
        return



    def go_offline():


        user_sockets.pop(
            sid,
            None
        )



        sockets = user_connections.get(
            user_id,
            set()
        )



        sockets.discard(
            sid
        )



        print(
            "❌ REMOVED",
            sid
        )


        print(
            "USER",
            user_id
        )


        print(
            "LEFT",
            sockets
        )



        if len(sockets) > 0:


            print(
                "🟢 STILL ONLINE"
            )

            return





        user_connections.pop(
            user_id,
            None
        )


        online_users[user_id]=False


        last_seen[user_id]=datetime.now(
            timezone.utc
        ).isoformat()



        print(
            "🔴 OFFLINE",
            user_id
        )



        callback(user_id)





    timer=threading.Timer(
        delay,
        go_offline
    )


    disconnect_timers[user_id]=timer


    timer.start()