# participant_resolver.py
from app.inbox.models import ConversationParticipant
from app.models.user import User
from app.storage.service import get_file_url

from .participant_result import ParticipantResult


class ParticipantResolver:

    @staticmethod
    def get(
        conversation_id: int,
        user_id: int,
    ) -> ParticipantResult | None:

        participants = ConversationParticipant.query.filter_by(
            conversation_id=conversation_id,
        ).all()

        if not participants:
            return None

        # Saved Messages
        if len(participants) == 1 and participants[0].user_id == user_id:
            return ParticipantResult(
                other_user_id=user_id,
                username="Saved Messages",
                name="Saved Messages",
                avatar=None,
                is_saved_messages=True,
            )

        other = next(
            (p for p in participants if p.user_id != user_id),
            None,
        )

        if not other:
            return None

        user = User.query.get(other.user_id)


        if not user:
            return ParticipantResult(
                other_user_id=other.user_id,
                username="deleted_user",
                name="Deleted User",
                avatar=None,
                is_saved_messages=False,
                is_deleted=True,
            )

        return ParticipantResult(
            other_user_id=user.id,
            username=user.username,
            name="Deleted User" if user.is_deleted else user.name,
            avatar=(
                None
                if user.is_deleted
                else (get_file_url(user.profile_picture) if user.profile_picture else None)
            ),
            is_saved_messages=False,
            is_deleted=user.is_deleted,
        )
