# app/inbox/services/messages/message_reaction_aggregator.py

from app.inbox.models.messages.message_reaction import MessageReaction
from app.models.user import User
from app.storage.service import get_file_url


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


        if user:

            grouped[emoji]["count"] += 1

            grouped[emoji]["users"].append(
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "avatar": (get_file_url(user.profile_picture)
                               if user.profile_picture else None),
                }
            )

        else:

            grouped[emoji]["users"].append(
                {
                    "id": r.user_id,
                    "name": "Unknown",
                    "username": None,
                    "avatar": None,
                }
            )

    return list(grouped.values())