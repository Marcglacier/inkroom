# app/inbox/services/inbox/get_inbox.py
from sqlalchemy import distinct

from app.extensions import db
from app.inbox.models import (
    Conversation,
    ConversationParticipant,
)
from app.inbox.services.conversations.conversation_builder import (
    build_conversation_card,
)


def get_inbox(user_id):
    print("🔥🔥🔥 GET_INBOX CALLED 🔥🔥🔥")
    print("\n========== GET INBOX ==========\nUSER:", user_id)

    convo_ids = [
        c[0]
        for c in (
            db.session.query(
                distinct(
                    ConversationParticipant.conversation_id
                )
            )
            .filter(
                ConversationParticipant.user_id == user_id
            )
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

        print("STATUS:", convo.status)

        card = build_conversation_card(
            convo,
            user_id,
        )

        if not card:
            continue

        print("✅ ADDING TO INBOX:", convo.id)

        results.append(card)

    results.sort(
        key=lambda c: c["last_message"]["created_at"],
        reverse=True,
    )

    print(
        "TOTAL INBOX ITEMS:",
        len(results),
        "\n================================\n",
    )

    return results