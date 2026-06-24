from flask_socketio import emit, join_room
from flask import request

from app.sockets.messaging import sid_to_user



def register_typing_events(socketio):



    @socketio.on("join_conversation")
    def join_conversation(data):


        conversation_id = data.get(
            "conversation_id"
        )


        if not conversation_id:
            return



        join_room(
            f"conversation_{conversation_id}"
        )



        print(
            "🔥 TYPING ROOM JOINED:",
            conversation_id
        )





    @socketio.on("typing_start")
    def typing_start(data):


        user_id = sid_to_user.get(
            request.sid
        )


        if not user_id:
            print(
                "❌ NO USER FOR TYPING",
                request.sid
            )
            return



        conversation_id = data.get(
            "conversation_id"
        )



        print(
            "⌨️ START TYPING",
            {
                "user":user_id,
                "conversation":conversation_id
            }
        )



        emit(

            "user:typing",

            {
                "user_id":user_id,
                "conversation_id":conversation_id
            },


            room=f"conversation_{conversation_id}",

            include_self=False

        )







    @socketio.on("typing_stop")
    def typing_stop(data):


        user_id = sid_to_user.get(
            request.sid
        )


        if not user_id:
            return



        conversation_id = data.get(
            "conversation_id"
        )



        print(
            "⌨️ STOP TYPING",
            {
                "user":user_id,
                "conversation":conversation_id
            }
        )



        emit(

            "user:stop_typing",

            {
                "user_id":user_id,
                "conversation_id":conversation_id
            },


            room=f"conversation_{conversation_id}",

            include_self=False

        )