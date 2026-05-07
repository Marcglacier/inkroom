# app/inbox/views/clear_conversation.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.extensions import db
from app.inbox.models.conversation_clear import ConversationClear


class ClearConversationAPI(MethodView):

    @jwt_required()
    def delete(self, conversation_id):

        user_id = int(get_jwt_identity())

        existing = ConversationClear.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()

        # -------------------------
        # UPDATE EXISTING CLEAR
        # -------------------------
        if existing:
            existing.cleared_at = datetime.utcnow()

        # -------------------------
        # CREATE CLEAR RECORD
        # -------------------------
        else:
            clear = ConversationClear(
                conversation_id=conversation_id,
                user_id=user_id
            )

            db.session.add(clear)

        db.session.commit()

        return {
            "message": "conversation cleared"
        }, 200