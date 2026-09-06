# app/inbox/services/archive/archive_conversation_service.py
from app.extensions import db
from app.inbox.models.conversations.conversation_archive import ( ConversationArchive, )
from flask import abort
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )

class ArchiveConversationService:

    def __init__(
        self,
        user_id: int,
        conversation_id: int,
    ):
        self.user_id = user_id
        self.conversation_id = conversation_id

    def execute(self):
        print("STEP 1")
        ConversationGuard.require_participant(
            self.conversation_id,
            self.user_id,
        )
        print("STEP 2")
        archive = self._find_archive()
        print("STEP 3", archive)

        if archive:
            abort( 409, description="Conversation already archived." )      
        print("STEP 4")
        archive = ConversationArchive(
            user_id=self.user_id,
            conversation_id=self.conversation_id,
        )

        db.session.add(archive)
        db.session.commit()

        return archive

    def _find_archive(self):

        return (
            ConversationArchive.query
            .filter_by(
                user_id=self.user_id,
                conversation_id=self.conversation_id,
            )
            .first()
        )