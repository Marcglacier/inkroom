# app/inbox/services/messages/read_receipt_policy.py

from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.models.user import User
from app.inbox.services.settings.restriction_policy import (
    RestrictionPolicy,
)
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

class ReadReceiptPolicy:
    def __init__(self, conversation_id: int):
        self.conversation_id = conversation_id
        self._visible = None

    @property
    def visible(self) -> bool:
        if self._visible is None:
            self._visible = self._resolve_visibility()

        return self._visible

    def _resolve_visibility(self) -> bool:
        participants = ConversationParticipant.query.filter_by(
            conversation_id=self.conversation_id,
        ).all()

        user_ids = {
            participant.user_id
            for participant in participants
            if participant.user_id is not None
        }

        if len(user_ids) != 2:
            return False

        users = User.query.filter(
            User.id.in_(user_ids)
        ).all()

        if (
            len(users) != 2
            or {user.id for user in users} != user_ids
        ):
            return False

        if not all(user.show_read_receipts for user in users):
            return False

        user_a_id, user_b_id = tuple(user_ids)

        return (
            not RestrictionPolicy.restricts_either_user(
                user_a_id,
                user_b_id,
            )
            and not BlockPolicy.blocks_either_user(
                user_a_id,
                user_b_id,
            )
        )

    def message_status(self, message) -> str:
        if message.status == "read" and not self.visible:
            return "delivered"

        return message.status

    def read_at(self, message):
        if not self.visible:
            return None

        return message.read_at
