# app/inbox/services/archive/restore_conversation_service.py
from app.extensions import db
from flask import abort
from app.inbox.models.conversations.conversation_archive import ( ConversationArchive, )
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )


class RestoreConversationService:

    def __init__(
        self,
        user_id: int,
        conversation_id: int,
    ):
        self.user_id = user_id
        self.conversation_id = conversation_id

    def execute(self):
        ConversationGuard.require_participant( self.conversation_id, self.user_id, )
        archive = self._find_archive()
        if not archive: 
            abort( 
                404, 
                description="Conversation is not archived.", )

        db.session.delete(archive)
        db.session.commit()
        return archive

    def _find_archive(self):

        return (
            ConversationArchive.query
            .filter_by( user_id=self.user_id, conversation_id=self.conversation_id, )
            .first()
        )