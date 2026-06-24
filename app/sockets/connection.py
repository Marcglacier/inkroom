from flask_socketio import (
    join_room,
    emit
)

from flask_jwt_extended import decode_token
from flask import request

from app.sockets.presence_store import (
    set_online,
    set_offline_later,
    online_users,
    last_seen
)

from app.sockets.messaging import (
    active_chambers,
    sid_to_user
)
from app.extensions import db

from app.inbox.models.message import Message

from app.inbox.models.conversation_participant import (
    ConversationParticipant
)

print(
    "🚨 CONNECTION EVENTS FILE LOADED"
)



def register_connection_events(socketio):



  @socketio.on("connect")
  def handle_connect(auth):


    print(
        "\n🔥 SOCKET CONNECT ATTEMPT"
    )


    print(
        "AUTH:",
        auth
    )


    token = None


    if auth and isinstance(auth, dict):

        token = auth.get(
            "token"
        )


    if not token:


        print(
            "❌ NO TOKEN"
        )


        return False


    try:


        decoded = decode_token(
            token
        )


        user_id = int(
            decoded["sub"]
        )



        set_online(
            user_id,
            request.sid
        )



        #
        # SENT -> DELIVERED
        #

        conversation_ids = [

            p.conversation_id

            for p in

            ConversationParticipant.query.filter_by(
                user_id=user_id
            ).all()

        ]


        messages = (

            Message.query

            .filter(
                Message.conversation_id.in_(
                    conversation_ids
                ),

                Message.sender_id != user_id,

                Message.status == "sent"
            )

            .all()

        )


        print(
            "📦 SENT MESSAGES FOUND:",
            len(messages)
        )


        for msg in messages:


            msg.status = "delivered"


            socketio.emit(

                "message:status",

                {

                    "message_id": msg.id,

                    "status": "delivered"

                },

                room=f"user_{msg.sender_id}"

            )


            print(
                "📦 DELIVERED:",
                msg.id
            )


        db.session.commit()



        join_room(
            f"user_{user_id}"
        )


        join_room(
            "global_feed"
        )



        print(
            "🟢 CONNECT ONLINE:",
            user_id
        )


        print(
            "ONLINE:",
            online_users
        )



        emit(

            "presence:test",

            {
                "hello":"world",
                "user_id":user_id
            }

        )



        emit(

            "presence:status",

            {
                "user_id":user_id,
                "online":True,
                "last_seen":None
            }

        )



        socketio.emit(

            "presence:status",

            {
                "user_id":user_id,
                "online":True,
                "last_seen":None
            }

        )



        print(
            "📦 SENDING ONLINE SNAPSHOT"
        )


        for uid,status in online_users.items():


            emit(

                "presence:status",

                {
                    "user_id":uid,
                    "online":status,
                    "last_seen":last_seen.get(uid)
                }

            )



        print(
            "✅ CONNECT COMPLETE"
        )


        return True



    except Exception as e:


        print(
            "❌ SOCKET AUTH ERROR"
        )


        print(e)


        return False








  @socketio.on("presence:request")
  def presence_request():


        print(
            "📡 PRESENCE SNAPSHOT REQUEST"
        )


        for uid,status in online_users.items():


            emit(

                "presence:status",

                {
                    "user_id":uid,
                    "online":status,
                    "last_seen":last_seen.get(uid)
                }

            )









  @socketio.on("disconnect")
  def handle_disconnect():


        print(
            "\n🔥🔥 SOCKET DISCONNECTED"
        )


        print(
            "SID:",
            request.sid
        )



        #
        # REMOVE ACTIVE CHAT
        #

        user_id = sid_to_user.pop(
            request.sid,
            None
        )



        if user_id:


            active_chambers.pop(
                user_id,
                None
            )


            print(
                "🧹 REMOVED CHAT USER:",
                user_id
            )



        #
        # START OFFLINE TIMER
        #

        set_offline_later(

            request.sid,


            lambda uid:


                socketio.emit(

                    "presence:status",

                    {
                        "user_id":uid,
                        "online":False,
                        "last_seen":last_seen.get(uid)
                    }

                )

        )



        print(
            "⏳ OFFLINE TIMER STARTED"
        )