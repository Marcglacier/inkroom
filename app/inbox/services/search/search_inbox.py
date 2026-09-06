# app/inbox/services/search/search_inbox.py
from app.inbox.queries.search_inbox_query import (
    search_inbox_messages,
)


class SearchInboxService:

    def __init__(
        self,
        user_id: int,
        text: str,
    ):
        self.user_id = user_id
        self.text = text

    def execute(self):
        return search_inbox_messages(
            self.user_id,
            self.text,
        )