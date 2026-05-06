# app/inbox/views/edit_message.py

from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.inbox.models.message import Message


class EditMessageAPI(MethodView):

    @jwt_required()
    def put(self, message_id):

        user_id = int(get_jwt_identity())
        data = request.get_json()

        message = Message.query.get_or_404(message_id)

        # only sender can edit
        if message.sender_id != user_id:
            return {"error": "You can only edit your own messages"}, 403

        message.content = data["content"]
        message.edited = True

        db.session.commit()

        return {
            "message": "Message updated",
            "id": message.id,
            "content": message.content
        }