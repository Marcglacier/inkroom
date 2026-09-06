# app/inbox/services/conversations/delete_conversation_service.py

from app.inbox.services.conversations.lifecycle.clear_conversation_service import (
    ClearConversationService,
)

from app.inbox.services.conversations.lifecycle.hide_conversation_service import (
    HideConversationService,
)


class DeleteConversationService:

    def __init__(
        self,
        conversation_id: int,
        user_id: int,
    ):
        self.conversation_id = conversation_id
        self.user_id = user_id

    def execute(self):

        ClearConversationService(
            self.conversation_id,
            self.user_id,
        ).execute()

        HideConversationService(
            self.conversation_id,
            self.user_id,
        ).execute()

        return {
            "conversation_id": self.conversation_id,
            "status": "deleted",
        }