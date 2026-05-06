# app/inbox/services/query_helpers.py
def conversation_key(user1, user2):
    return tuple(sorted([user1, user2]))