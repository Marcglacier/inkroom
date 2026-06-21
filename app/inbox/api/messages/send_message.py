import os
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.conversation import Conversation
from app.inbox.serializers.message_serializer import MessageSerializer

UPLOAD_FOLDER = "media/messages"


class SendMessageAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        sender_id = int(get_jwt_identity())
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # -----------------------------
        # JSON SUPPORT
        # -----------------------------
        data = request.get_json(silent=True) or {}

        content = data.get("content")
        reply_to_message_id = data.get("reply_to_message_id")
        

        # -----------------------------
        # FORM SUPPORT (for media)
        # -----------------------------
        if request.form:
            content = request.form.get("content", content)
            reply_to_message_id = request.form.get(
                "reply_to_message_id", reply_to_message_id
            )

        file = request.files.get("media")

        media_url = None
        media_type = None

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            file.save(filepath)

            media_url = f"/{UPLOAD_FOLDER}/{filename}"
            media_type = file.mimetype

        conversation = Conversation.get_or_create(sender_id, user_id)

        message = Message(
            conversation_id=conversation.id,
            sender_id=sender_id,
            content=content,
            media_url=media_url,
            media_type=media_type,
            reply_to_message_id=reply_to_message_id
        )

        db.session.add(message)
        db.session.commit()


        payload = MessageSerializer(
            message
        ).to_dict()


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


        print(
            "🔥 EMIT COMPLETE"
        )

        return jsonify(message.to_dict()), 201