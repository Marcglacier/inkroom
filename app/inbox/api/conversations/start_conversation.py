from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db

from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.models.conversation_request import ConversationRequest


class StartConversationAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        current_user = int(get_jwt_identity())
        user_id = int(user_id)


        if current_user == user_id:
            return {
                "error": "Cannot summon yourself"
            },400



        # =========================
        # CHECK EXISTING CHAMBER
        # =========================

        my_conversations = (
            ConversationParticipant.query
            .filter_by(
                user_id=current_user
            )
            .all()
        )


        for item in my_conversations:

            exists = (
                ConversationParticipant.query
                .filter_by(
                    conversation_id=item.conversation_id,
                    user_id=user_id
                )
                .first()
            )


            if exists:

                conversation = Conversation.query.get(
                    item.conversation_id
                )


                return {

                    "conversation_id":
                        conversation.id,

                    "status":
                        conversation.status

                },200




        # =========================
        # CREATE REQUEST CHAMBER
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

            "conversation_id":
                conversation.id,

            "status":
                "request_sent"

        },201