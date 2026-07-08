from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.models.user import User
from app.models.profile import Profile
from app.storage.service import get_file_url


class ConversationDetailAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())
        conversation = Conversation.query.get_or_404(
            conversation_id
        )
        participant = ConversationParticipant.query.filter(
            ConversationParticipant.conversation_id == conversation_id,
            ConversationParticipant.user_id != user_id
        ).first()
        if not participant:
            return {
                "error":"No raven found"
            },404
        user = User.query.get(
            participant.user_id
        )
        profile = Profile.query.filter_by(
            user_id=user.id
        ).first()
        print("OTHER USER:",)
        print("PROFLE:", profile)
        print("AVATAR:", profile.avatar_url if profile else None)

        return {

            "id": user.id,
            "name": user.name,
            "username": user.username,
            "avatar": (
                get_file_url(user.profile_picture)
                if user.profile_picture
                else None
            ),

        },200