import os


from flask.views import MethodView
from flask import (
    request,
    jsonify
)


from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


from werkzeug.utils import secure_filename



from app.sockets.presence_store import (
    online_users
)


from app.sockets.messaging import (
    active_chambers
)



from app.extensions import (
    db,
    socketio
)



from app.inbox.models.message import (
    Message
)


from app.inbox.models.conversation import (
    Conversation
)


from app.inbox.serializers.message_serializer import (
    MessageSerializer
)




UPLOAD_FOLDER = "media/messages"






class SendMessageAPI(MethodView):




    @jwt_required()
    def post(self, user_id):



        sender_id = int(
            get_jwt_identity()
        )



        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )





        data = request.get_json(
            silent=True
        ) or {}



        content = data.get(
            "content"
        )


        reply_to_message_id = data.get(
            "reply_to_message_id"
        )





        if request.form:


            content = request.form.get(
                "content",
                content
            )


            reply_to_message_id = request.form.get(
                "reply_to_message_id",
                reply_to_message_id
            )






        file = request.files.get(
            "media"
        )



        media_url = None

        media_type = None





        if file:


            filename = secure_filename(
                file.filename
            )


            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )


            file.save(
                filepath
            )


            media_url = f"/{UPLOAD_FOLDER}/{filename}"

            media_type = file.mimetype







        conversation = Conversation.get_or_create(

            sender_id,

            user_id

        )






        message = Message(

            conversation_id = conversation.id,

            sender_id = sender_id,

            content = content,

            media_url = media_url,

            media_type = media_type,

            reply_to_message_id = reply_to_message_id

        )






        db.session.add(
            message
        )


        db.session.commit()







        payload = MessageSerializer(
            message
        ).to_dict()







        #
        # REAL LIVE STATE CHECK
        #



        receiver_id = int(
            user_id
        )



        receiver_online = (

            online_users.get(

                receiver_id,

                False

            )

            is True

        )





        receiver_in_chat = (

            active_chambers.get(

                receiver_id

            )

            ==

            conversation.id

        )








        #
        # STATUS DECISION
        #


        if receiver_in_chat:


            status = "read"



        elif receiver_online:


            status = "delivered"



        else:


            status = "sent"






        payload["status"] = status







        print(
            "\n======================"
        )


        print(
            "🔥 MESSAGE STATUS:",
            status
        )


        print(
            "👤 RECEIVER:",
            receiver_id
        )


        print(
            "🟢 RECEIVER ONLINE:",
            receiver_online
        )


        print(
            "💬 RECEIVER IN CHAT:",
            receiver_in_chat
        )


        print(
            "👁 ONLINE MAP:",
            online_users
        )


        print(
            "👁 ACTIVE CHAMBERS:",
            active_chambers
        )


        print(
            "======================\n"
        )







        print(
            "🔥 EMITTING MESSAGE:",
            payload
        )



        print(
            "🔥 TARGET ROOM:",
            f"conversation_{conversation.id}"
        )








        socketio.emit(

            "message:new",

            payload,

            room=f"conversation_{conversation.id}"

        )








        #
        # UPDATE SENDER STATUS
        #

        socketio.emit(

            "message:status",

            {

                "message_id": message.id,

                "status": status

            },

            room=f"user_{sender_id}"

        )





        print(
            "🔥 EMIT COMPLETE"
        )




        return jsonify(
            payload
        ), 201