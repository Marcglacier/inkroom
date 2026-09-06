# app/inbox/services/conversations/resolvers/last_message_result.py

from dataclasses import dataclass

from app.inbox.models.messages.message import Message


@dataclass(slots=True)
class LastMessageResult:
    last_message: Message | None