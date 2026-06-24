from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db

from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_request import ConversationRequest

from app.models.follow import Follow

class StartConversationAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        current_user = int(get_jwt_identity())
        user_id = int(user_id)

        if current_user == user_id:
            return {
                "error": "Cannot summon yourself"
            }, 400

        # =========================
        # CHECK EXISTING CONVERSATION
        # =========================

        conversation = Conversation.find_between_users(
            current_user,
            user_id
        )

        if conversation:
            return {
                "conversation_id": conversation.id,
                "status": conversation.status
            }, 200

        # =========================
        # CHECK MUTUAL STATUS
        # =========================

        i_follow_them = Follow.query.filter_by(
            follower_id=current_user,
            following_id=user_id
        ).first()

        they_follow_me = Follow.query.filter_by(
            follower_id=user_id,
            following_id=current_user
        ).first()

        is_mutual = (
            i_follow_them is not None and
            they_follow_me is not None
        )

        # =========================
        # CREATE ACTIVE CHAT
        # =========================

        if is_mutual:

            conversation = Conversation.get_or_create(
                current_user,
                user_id
            )

            return {
                "conversation_id": conversation.id,
                "status": "active"
            }, 201

        # =========================
        # CREATE REQUEST CHAT
        # =========================

        conversation = Conversation.create_request(
            current_user,
            user_id
        )

        request = ConversationRequest(
            sender_id=current_user,
            receiver_id=user_id,
            conversation_id=conversation.id
        )

        db.session.add(request)
        db.session.commit()

        return {
            "conversation_id": conversation.id,
            "status": "pending"
        }, 201