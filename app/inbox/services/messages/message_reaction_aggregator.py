# app/inbox/services/messages/message_reaction_aggregator.py
from app.inbox.models.message_reaction import MessageReaction
from app.models.user import User


def build_reactions(message_id):
    reactions = MessageReaction.query.filter_by(
        message_id=message_id
    ).all()

    grouped = {}

    for r in reactions:
        emoji = r.reaction

        if emoji not in grouped:
            grouped[emoji] = {
                "emoji": emoji,
                "count": 0,
                "users": []
            }

        user = User.query.get(r.user_id)

        grouped[emoji]["count"] += 1
        grouped[emoji]["users"].append(
            user.username if user else str(r.user_id)
        )

    return list(grouped.values())