import os
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.sockets.presence_store import online_users
from app.sockets.messaging import active_chambers
from app.extensions import db, socketio
from app.inbox.models import Message, Conversation
from app.inbox.serializers.message_serializer import MessageSerializer
from app.inbox.services.messages.message_status import (get_message_status,)

UPLOAD_FOLDER = "media/messages"

class SendMessageAPI(MethodView):
    @jwt_required()
    def post(self, user_id):
        sender_id = int(get_jwt_identity())
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        data = request.get_json(silent=True) or {}
        content = data.get("content")
        reply_to = data.get("reply_to_message_id")

        if request.form:
            content = request.form.get("content", content)
            reply_to = request.form.get("reply_to_message_id", reply_to)

        file = request.files.get("media")
        media_url, media_type = None, None
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            media_url, media_type = f"/{UPLOAD_FOLDER}/{filename}", file.mimetype

        convo = Conversation.get_or_create(sender_id, user_id)
        print("\n============================")
        print("CONVERSATION:", convo.id, "STATUS:", convo.status)

        if convo.status == "rejected":
            print("🚫 MESSAGE BLOCKED (rejected)")
            return jsonify({"error": "Message request declined"}), 403

        msg = Message(conversation_id=convo.id, sender_id=sender_id,
                      content=content, media_url=media_url,
                      media_type=media_type, reply_to_message_id=reply_to)
        db.session.add(msg); db.session.commit()

        if convo.status == "pending":
            convo.status = "pending_request"; db.session.commit()
            print("📨 CONVERSATION MOVED TO PENDING_REQUEST")

        payload = MessageSerializer(msg).to_dict()
        receiver_id = int(user_id)

        status, online, in_chat = get_message_status(
         receiver_id,
         convo.id,
         convo.status,
        )

        payload["status"] = status
        print(f"\n🔥 MESSAGE STATUS: {status}\n👤 RECEIVER: {receiver_id}\n🟢 ONLINE: {online}\n💬 IN CHAT: {in_chat}\n🔥 EMITTING MESSAGE:", payload)

        socketio.emit("message:new", payload, room=f"conversation_{convo.id}")
        socketio.emit("message:status", {"message_id": msg.id, "status": status}, room=f"user_{sender_id}")
        print("🔥 EMIT COMPLETE\n============================\n")

        return jsonify(payload), 201
