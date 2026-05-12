# app/inbox/services/search/search_inbox.py
from app.inbox.queries.search_inbox_query import search_inbox_messages


def search_inbox(user_id, text):
    return search_inbox_messages(user_id, text)