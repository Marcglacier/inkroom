# app/inbox/services/archive/fetch_archived_conversations_service.py

from app.inbox.models.conversations.conversation_archive import ConversationArchive

class FetchArchivedConversationsService:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self):
        pass