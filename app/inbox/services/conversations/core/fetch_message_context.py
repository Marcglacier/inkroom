# app/inbox/services/messages/fetch_message_context.py
from app.extensions import db
from app.inbox.models.messages.message import Message
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import build_reactions
from app.inbox.serializers.message_media_serializer import MessageMediaSerializer


class FetchMessageContextService:
    def __init__(
        self, conversation_id: int, message_id: int, user_id: int, ):
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.user_id = user_id

    def execute(self):
        target = (
            Message.query
            .filter_by(
                id=self.message_id,
                conversation_id=self.conversation_id,
            )
            .first()
        )

        if not target:
            return None

        # Fetch messages before and after the target message
        older = (  Message.query
            .filter(
               Message.conversation_id == self.conversation_id,
               Message.created_at < target.created_at,
               Message.deleted_for_everyone.is_(False),
            )
            .order_by(Message.created_at.desc()) .limit(7) .all()
        )

        older.reverse()

        newer = ( Message.query
            .filter(
                Message.conversation_id == self.conversation_id,
                Message.created_at > target.created_at,
                Message.deleted_for_everyone.is_(False),
            )
            .order_by(Message.created_at.asc()) .limit(7) .all()
        )
        messages = [ *older, target, *newer, ]

        return self._serialize(messages)

    def _serialize(self, messages):
        message_cache = {} ; user_cache = {} ; serialized = []
        for message in messages:

         # Skip messages deleted only for this user
         if self.user_id in (message.deleted_for_users or []):
            continue
         sender = self._get_user( user_cache, message.sender_id, )
         sender_username = ( sender.username if sender else "deleted_user" )
         sender_name = ( sender.name if sender else "Deleted User" )
         reply_data = None

         if message.reply_to_message_id:
            replied_msg = self._get_message( message_cache, message.reply_to_message_id, )

            if ( replied_msg and not replied_msg.deleted_for_everyone ):
                reply_sender = self._get_user( user_cache, replied_msg.sender_id, )

                reply_data = { "id": replied_msg.id, "content": replied_msg.content,
                    "sender_id": replied_msg.sender_id, "sender_name": (
                        reply_sender.name if reply_sender else "Deleted User" ),

                    "sender_username": (
                        reply_sender.username
                        if reply_sender else "deleted_user" ),
                }

         reactions = build_reactions(message.id)
         media = [ MessageMediaSerializer(m).to_dict() for m in message.media ]

         serialized.append({ "id": message.id, "content": message.content,
            "message_type": message.message_type, "system_event": message.system_event,
            "target_message_id": message.target_message_id, "media": media, "sender_id": message.sender_id,
            "sender_username": sender_username, "sender_name": sender_name, "created_at": message.created_at,
            "edited": message.edited, "status": message.status, "delivered_at": message.delivered_at,
            "read_at": message.read_at, "is_sender": ( message.sender_id == self.user_id ), "is_forwarded": message.is_forwarded,
            "forwarded_from_id": message.forwarded_from_id, "deleted_for_everyone": ( message.deleted_for_everyone ),
            "reply_to": reply_data, "reactions": reactions,  })
            
        return serialized

    def _get_user(self, user_cache, user_id):
      if user_id not in user_cache:
            user_cache[user_id] = User.query.get(user_id)

      return user_cache[user_id]    

    def _get_message(self, message_cache, message_id):
      if message_id not in message_cache:
            message_cache[message_id] = Message.query.get(message_id)

      return message_cache[message_id]