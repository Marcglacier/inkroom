# app/inbox/services/inbox/get_inbox.py
from sqlalchemy import distinct
from app.extensions import db
from app.inbox.models import Conversation, ConversationParticipant
from app.inbox.services.conversations.core.conversation_builder import ConversationCardBuilder
from app.inbox.models.conversations.conversation_hide import ConversationHide
from app.inbox.models.conversations.conversation_archive import ( ConversationArchive, )

def get_inbox(user_id):
    print("🔥🔥🔥 GET_INBOX CALLED 🔥🔥🔥")
    print("\n========== GET INBOX ==========\nUSER:", user_id)

    convo_ids = [
        c[0]
        for c in (
            db.session.query(
                distinct(ConversationParticipant.conversation_id)
            )
            .filter(ConversationParticipant.user_id == user_id)
            .all()
        )
    ]

    results = []

    for convo_id in convo_ids:
        print("\n--------------------")
        print("CHECKING CONVO:", convo_id)

        convo = Conversation.query.get(convo_id)
        if not convo:
            print("❌ CONVO NOT FOUND")
            continue

        # check hidden before building card
        hidden = ConversationHide.query.filter_by(
            conversation_id=convo_id, user_id=user_id
        ).first()
        if hidden:
            print("🙈 Conversation hidden")
            continue
        print("STATUS:", convo.status)

        archived = ConversationArchive.query.filter_by(
            conversation_id=convo_id, user_id=user_id,).first()

        if archived:
            print("📦 Conversation archived")
            continue     

        card = ConversationCardBuilder(convo, user_id).build()
        if not card:
            continue
      
        print("✅ ADDING TO INBOX:", convo.id)
        results.append(card)

    # sort once, after building
    results.sort(
        key=lambda c: (
            c["is_pinned"],
            c["last_message"]["created_at"]
            if c["last_message"]  else "",
        ),
        reverse=True,
    )
    print("TOTAL INBOX ITEMS:", len(results), "\n================================\n")
    return results