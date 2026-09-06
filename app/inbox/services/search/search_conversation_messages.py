# app/inbox/services/search/search_conversation_messages.py

from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_clear import ConversationClear


class SearchConversationMessagesService:

    def __init__(
        self,
        user_id: int,
        conversation_id: int,
        text: str,
    ):
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.text = text.strip()

    def execute(self):

        if not self.text:
            return []

        query = self._build_query()
        messages = query.all()
        visible_messages = self._filter_visible_messages( messages )

        return self._serialize(visible_messages)

    def _build_query(self):

        query = ( Message.query
            .filter(
                Message.conversation_id == self.conversation_id,
                Message.content.ilike(f"%{self.text}%"),
                Message.deleted_for_everyone.is_(False),
            )
        )
        last_clear = self._get_last_clear()

        if last_clear: query = query.filter( Message.created_at > last_clear.cleared_at )

        return ( query .order_by(Message.created_at.desc()) )

    def _get_last_clear(self):

        return (
            ConversationClear.query
                .filter_by( user_id=self.user_id, conversation_id=self.conversation_id, )
                .order_by( ConversationClear.cleared_at.desc() )
                .first() )
    
    def _filter_visible_messages(self, messages):

        return [
            message
            for message in messages
            if self.user_id not in (message.deleted_for_users or [])
    ]

    def _serialize(self, messages):

        serialized = []

        for message in messages:

            serialized.append({
                "id": message.id, "conversation_id": message.conversation_id,
                "content": message.content, "message_type": message.message_type,
                "sender_id": message.sender_id, "created_at": message.created_at,
            })

        return serialized