from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.models.user import User
from app.models.profile import Profile
from app.storage.service import get_file_url


class ConversationDetailAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())

        ConversationGuard.require_participant(
            conversation_id,
            user_id,
        )

        # -------------------------------------------------
        # Find the other participant.
        #
        # IMPORTANT:
        # A deleted user's participant row has user_id=NULL.
        # SQL `NULL != user_id` does NOT evaluate to True,
        # so we cannot use the old filter directly.
        # -------------------------------------------------
        participants = ConversationParticipant.query.filter_by(
            conversation_id=conversation_id
        ).all()

        participant = next(
            (
                p
                for p in participants
                if p.user_id != user_id
            ),
            None,
        )

        if not participant:
            return {
                "error": "No raven found"
            }, 404

        #================= Deleted user ====================
        if participant.user_id is None:
            return {
                "id": None,
                "name": "Deleted User",
                "username": None,
                "avatar": None,
                "deleted": True,
            }, 200

        #================= Normal user ====================

        user = User.query.get(
            participant.user_id
        )

        # -------------------------------------------------
        # Safety fallback:
        # Participant exists but User record is gone.
        # -------------------------------------------------
        if not user:
            return {
                "id": participant.user_id,
                "name": "Deleted User",
                "username": None,
                "avatar": None,
                "deleted": True,
            }, 200

        # -------------------------------------------------
        # Profile
        # -------------------------------------------------
        profile = Profile.query.filter_by(
            user_id=user.id
        ).first()

        print("OTHER USER:", user)
        print("PROFILE:", profile)
        print(
            "AVATAR:",
            profile.avatar_url if profile else None
        )

        # -------------------------------------------------
        # Normal user response
        # -------------------------------------------------
        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "avatar": (
                get_file_url(user.profile_picture)
                if user.profile_picture
                else None
            ),
            "deleted": False,
        }, 200