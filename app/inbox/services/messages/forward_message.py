# app/inbox/services/messages/forward_message.py
from datetime import datetime

from app.extensions import db, socketio

from app.inbox.models.messages.message import Message
from app.inbox.models.messages.message_media import MessageMedia
from app.inbox.models.messages.message_link import MessageLink

from app.inbox.services.conversations.core.conversation_service import (
    ConversationService,
)

from app.inbox.services.messages.message_status import (
    get_message_status,
)

from app.inbox.serializers.message_serializer import MessageSerializer


class ForwardMessageService:

    def __init__(
        self,
        sender_id: int,
        message_id: int,
        to_user_id: int,
    ):
        self.sender_id = sender_id
        self.message_id = message_id
        self.to_user_id = to_user_id

        self.original = None
        self.conversation = None
        self.new_message = None
        self.status = None
        self.payload = None

    # =========================================================
    # PUBLIC
    # =========================================================

    def execute(self):
        self._load_original()
        self._validate_original()
        self._get_conversation()
        self._create_forwarded_message()
        self._clone_media()
        self._clone_links()
        self._commit_message()
        self._update_status()
        self._build_payload()
        self._emit_events()

        return self.payload, 201

    # =========================================================
    # ORIGINAL MESSAGE
    # =========================================================

    def _load_original(self):
        self.original = Message.query.get(self.message_id)

        if not self.original:
            raise ValueError("Message not found")

    def _validate_original(self):

        if self.original.deleted_for_everyone:
            raise ValueError(
                "Deleted messages cannot be forwarded"
            )

        if self.sender_id in (
            self.original.deleted_for_users or []
        ):
            raise ValueError(
                "You cannot forward this message"
            )

    # =========================================================
    # CONVERSATION
    # =========================================================

    def _get_conversation(self):
        self.conversation = ConversationService.get_or_create(
            self.sender_id,
            self.to_user_id,
        )

    # =========================================================
    # MESSAGE
    # =========================================================

    def _create_forwarded_message(self):

        self.new_message = Message(
            conversation_id=self.conversation.id,
            sender_id=self.sender_id,

            content=self.original.content,
            backup_content=self.original.content,

            # Internal only.
            forwarded_from_id=self.original.id,
            is_forwarded=True,

            edited=False,
            status="sent",
            created_at=datetime.utcnow(),
        )

        db.session.add(self.new_message)
        db.session.flush()

    # =========================================================
    # MEDIA
    # =========================================================

    def _clone_media(self):

        for media in self.original.media:
            self._clone_single_media(media)

    def _clone_single_media(self, media):

        cloned = MessageMedia(
            message_id=self.new_message.id,

            # Core
            object_key=media.object_key,
            filename=media.filename,
            mime_type=media.mime_type,
            size=media.size,

            # General
            media_kind=media.media_kind,
            waveform=media.waveform,

            # Audio
            title=media.title,
            artist=media.artist,
            album=media.album,
            duration=media.duration,
            cover_object_key=media.cover_object_key,

            # Video
            video_width=media.video_width,
            video_height=media.video_height,
            thumbnail_object_key=media.thumbnail_object_key,
        )

        db.session.add(cloned)

    # =========================================================
    # LINKS
    # =========================================================

    def _clone_links(self):

        for link in self.original.links:
            self._clone_single_link(link)

    def _clone_single_link(self, link):

        cloned = MessageLink(
            message_id=self.new_message.id,

            url=link.url,
            normalized_url=link.normalized_url,

            # Preview
            title=link.title,
            description=link.description,
            image_url=link.image_url,

            site_name=link.site_name,
            domain=link.domain,
            platform=link.platform,
            content_type=link.content_type,

            fetched_at=link.fetched_at,
            created_at=datetime.utcnow(),
        )

        db.session.add(cloned)

    # =========================================================
    # DATABASE
    # =========================================================

    def _commit_message(self):
        db.session.commit()

    # =========================================================
    # STATUS
    # =========================================================

    def _update_status(self):

        (
            self.status,
            online,
            in_chat,
        ) = get_message_status(
            self.to_user_id,
            self.conversation.id,
            self.conversation.status,
        )

        self.new_message.status = self.status

        db.session.commit()
        db.session.refresh(self.new_message)

    # =========================================================
    # SERIALIZATION
    # =========================================================

    def _build_payload(self):

        self.payload = MessageSerializer(
            self.new_message,
            viewer_id=self.sender_id,
        ).to_dict()

        self.payload["message"] = "forwarded"

    # =========================================================
    # SOCKET
    # =========================================================

    def _emit_events(self):

        socketio.emit(
            "message:new",
            self.payload,
            room=f"conversation_{self.conversation.id}",
        )

        socketio.emit(
            "message:status",
            {
                "message_id": self.new_message.id,
                "status": self.status,
            },
            room=f"user_{self.sender_id}",
        )


# =============================================================
# PUBLIC SERVICE FUNCTION
# =============================================================

def forward_message(
    sender_id: int,
    message_id: int,
    to_user_id: int,
):
    try:

        service = ForwardMessageService(
            sender_id=sender_id,
            message_id=message_id,
            to_user_id=to_user_id,
        )

        return service.execute()

    except ValueError as exc:

        return {
            "error": str(exc)
        }, 404