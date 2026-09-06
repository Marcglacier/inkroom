# app/inbox/services/archive/get_archived_conversations_service.py
from sqlalchemy import distinct
from app.extensions import db
from app.inbox.models import  Conversation, ConversationParticipant
from app.inbox.models.conversations.conversation_archive import ConversationArchive
from app.inbox.services.conversations.core.conversation_builder import  ConversationCardBuilder
from app.inbox.models.conversations.conversation_hide import ConversationHide

class GetArchivedConversationsService:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self):

        convo_ids = self._conversation_ids()

        results = []

        for convo_id in convo_ids:

            if not self._is_archived(convo_id):
                continue

            if self._is_hidden(convo_id):
                continue
            conversation = Conversation.query.get(convo_id)

            if not conversation:
                continue

            card = ConversationCardBuilder(
                conversation,
                self.user_id,
            ).build()   

            if card:
                results.append(card)

        results.sort(
            key=lambda c: (
                c["last_message"]["created_at"]
                if c["last_message"]
                else ""
            ),
            reverse=True,
        )

        return results

    def _conversation_ids(self):

        return [
            c[0]
            for c in (
                db.session.query(
                    distinct(
                        ConversationParticipant.conversation_id
                    )
                )
                .filter(
                    ConversationParticipant.user_id
                    == self.user_id
                )
                .all()
            )
        ]

    def _is_archived(
        self, conversation_id: int,
    ):

        archive = (
            ConversationArchive.query
            .filter_by(
                user_id=self.user_id,
                conversation_id=conversation_id,
            )
            .first()
        )

        return archive is not None  
    def _is_hidden(
        self,  conversation_id: int, ):

        hidden = (
            ConversationHide.query
            .filter_by(
                user_id=self.user_id,
                conversation_id=conversation_id,
            )
            .first()
        )

        return hidden is not None      