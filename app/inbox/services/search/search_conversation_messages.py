# app/inbox/services/search/search_conversation_messages.py
from app.extensions import db
from app.inbox.models.message import Message
from app.inbox.models.conversation_clear import ConversationClear


def search_conversation(user_id, conversation_id, text: str):
    print(f"\n=== SEARCH DEBUG ===")
    print(f"User: {user_id} | Conv: {conversation_id} | Search: '{text}'")

    if not text or not text.strip():
        print("Empty search text")
        return []

    text = text.strip()

    # 1. Check last clear time
    last_clear = (
        ConversationClear.query
        .filter_by(user_id=user_id, conversation_id=conversation_id)
        .order_by(ConversationClear.cleared_at.desc())
        .first()
    )
    
    print(f"Last cleared at: {last_clear.cleared_at if last_clear else 'NEVER'}")

    # 2. Base query - find ALL matching messages
    base_query = Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.content.ilike(f"%{text}%")
    )
    
    total_matches = base_query.count()
    print(f"Total messages containing '{text}': {total_matches}")

    # 3. Apply clear filter
    query = base_query
    if last_clear:
        query = query.filter(Message.created_at > last_clear.cleared_at)
        print(f"Filtering messages after: {last_clear.cleared_at}")

    results = query.order_by(Message.created_at.desc()).all()
    
    print(f"Final results after filter: {len(results)}")
    for msg in results[:5]:   # print first 5
        print(f"  → {msg.created_at} | {msg.content[:80]}")

    print("=== END DEBUG ===\n")
    
    return results