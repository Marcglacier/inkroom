# app/inbox/services/messages/fetch_messages.py

from app.inbox.models.message import Message
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import build_reactions
from app.inbox.serializers.message_media_serializer import MessageMediaSerializer


def fetch_messages(conversation_id, current_user_id):
    

    query = (
        Message.query.filter_by(conversation_id=conversation_id)
        .order_by(Message.created_at.asc())
    )

    messages = []
    message_cache, user_cache = {}, {}

    def get_user(user_id):
        if user_id not in user_cache:
            user_cache[user_id] = User.query.get(user_id)
        return user_cache[user_id]

    def get_message(msg_id):
        if msg_id not in message_cache:
            message_cache[msg_id] = Message.query.get(msg_id)
        return message_cache[msg_id]


    for message in query:

        # Skip deleted messages
        if current_user_id in (message.deleted_for_users or []):
            continue


        sender = get_user(message.sender_id)
        sender_username = sender.username if sender else None


        # Build reply data
        reply_data = None

        if message.reply_to_message_id:
            replied_msg = get_message(message.reply_to_message_id)

            if replied_msg and not replied_msg.deleted_for_everyone:

                reply_sender = get_user(replied_msg.sender_id)

                reply_data = {
                    "id": replied_msg.id,
                    "content": replied_msg.content,
                    "sender_id": replied_msg.sender_id,
                    "sender_name": reply_sender.name if reply_sender else None,
                    "sender_username": reply_sender.username if reply_sender else None,
                }


        messages.append({

            "id": message.id,

            "content": message.content,


            # NEW MINIO MEDIA SYSTEM
            "media": [
                MessageMediaSerializer(media).to_dict()
                for media in message.media
            ],


            "sender_id": message.sender_id,

            "sender_username": sender_username,


            "created_at": message.created_at,

            "edited": message.edited,

            "status": message.status,


            "delivered_at": message.delivered_at,

            "read_at": message.read_at,


            "is_sender": (
                message.sender_id == current_user_id
            ),


            "is_forwarded": message.is_forwarded,

            "forwarded_from_id": message.forwarded_from_id,


            "deleted_for_everyone": (
                message.deleted_for_everyone
            ),


            "reply_to": reply_data,


            "reactions": build_reactions(message.id),

        })

    print(
     "DB MESSAGES:",
         [(m.id, m.content, m.created_at) for m in query])


    return messages