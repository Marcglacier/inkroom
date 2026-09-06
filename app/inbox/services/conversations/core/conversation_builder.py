# app/inbox/services/conversations/core/conversation_builder.py
from app.inbox.services.conversations.mutes.mute_guard import (  MuteGuard, )
from app.inbox.services.conversations.resolvers.last_message.last_message_resolver import (
    LastMessageResolver, 
)
from app.inbox.services.conversations.resolvers.clears.ConversationClearResolver import (
    ConversationClearResolver,
)
from app.inbox.services.conversations.pins.pin_guard import ( PinGuard, )
from app.inbox.services.conversations.resolvers.participants.participant_resolver import (
    ParticipantResolver
 )
from app.inbox.services.conversations.resolvers.participants.hides.conversation_visibility_guard import (
    ConversationVisibilityGuard,
)
from app.inbox.services.conversations.resolvers.last_message.unread.unread_count_resolver import (
    UnreadCountResolver,
)
from app.inbox.serializers.message_serializer import ( MessageSerializer, )
from app.inbox.serializers.conversation_card_serializer import ( ConversationCardSerializer, )

class ConversationCardBuilder:

    def __init__(
        self,
        conversation,
        user_id: int,
    ):
        self.conversation = conversation
        self.user_id = user_id

    def build(self):
        print("🔥🔥🔥 GET_INBOX CALLED 🔥🔥🔥")

        if not ConversationVisibilityGuard.should_show(
            self.conversation,
            self.user_id,
        ):
            return None

        participant = ParticipantResolver.get(
            self.conversation.id,
            self.user_id,
        )

        if not participant:
            return None

        is_pinned = PinGuard.is_pinned(
            self.conversation.id,
            self.user_id,
        )

        is_muted, mute_until = (
            MuteGuard.get_status(
                self.conversation.id,
                self.user_id,
            )
        )

        clear = ConversationClearResolver.get(
            self.conversation.id,
            self.user_id,
        )

        result = LastMessageResolver.get(
            self.conversation.id,
            self.user_id,
        )

        last_msg = result.last_message

        if not last_msg:
            if clear.was_cleared:
                return ConversationCardSerializer(
                    conversation=self.conversation,
                    participant=participant,
                    unread=0,
                    is_pinned=is_pinned,
                    is_muted=is_muted,
                    mute_until=mute_until,
                    last_message=None,
                ).to_dict()

            return None

        unread = UnreadCountResolver.get(
            self.conversation.id,
            self.user_id,
        )

        return ConversationCardSerializer(
            conversation=self.conversation,
            participant=participant,
            unread=unread,
            is_pinned=is_pinned,
            is_muted=is_muted,
            mute_until=mute_until,
            last_message=MessageSerializer(
                last_msg,
                viewer_id=self.user_id,
            ).to_dict(),
        ).to_dict()