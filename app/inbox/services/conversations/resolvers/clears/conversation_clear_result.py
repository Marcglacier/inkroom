# clear_result.py
from dataclasses import dataclass

from sqlalchemy.orm import Query

from app.inbox.models.conversations.conversation_clear import ConversationClear


@dataclass(slots=True)
class ConversationClearResult:
    clear: ConversationClear | None

    @property
    def was_cleared(self) -> bool:
        return self.clear is not None

    def apply(self, query: Query) -> Query:
        if not self.clear:
            return query

        return query.filter(
            query.column_descriptions[0]["entity"].created_at >
            self.clear.cleared_at
        )