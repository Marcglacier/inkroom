# participant_resolver.py
from app.inbox.models import ConversationParticipant
from app.models.user import User
from app.storage.service import get_file_url
from app.models.settings.user_block import UserBlock
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

        blocked_by_other = UserBlock.query.filter_by(
            blocker_id=other.user_id,
            blocked_id=user_id,
        ).first()

        if blocked_by_other:
            return ParticipantResult(
                other_user_id=other.user_id,
                username="deleted_user",
                name="Deleted User",
                avatar=None,
                is_saved_messages=False,
                is_deleted=False,
                is_blocked=True,
            )

        blocked_by_viewer = UserBlock.query.filter_by(
            blocker_id=user_id,
            blocked_id=other.user_id,
        ).first()

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
            is_blocker=bool(blocked_by_viewer),
        )
