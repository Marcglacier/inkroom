# app/infrastructure/celery/tasks.py

from .celery_app import celery

from app.auth.services.verification import (
    SendVerificationEmailService,
)


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def send_verification_email_task(
    self,
    email: str,
    verification_code: str,
):

    from app import create_app

    app = create_app()

    with app.app_context():

        SendVerificationEmailService(
            email=email,
            verification_code=verification_code,
        ).execute()


# ============================================================
# LINK PREVIEW BACKGROUND TASK
# ============================================================

@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def fetch_message_link_preview_task(
    self,
    message_id: int,
    raw_url: str,
    normalized_url: str,
):
    from app import create_app

    app = create_app()

    with app.app_context():

        from datetime import datetime

        from app.extensions import db, socketio
        from app.inbox.models.messages.message import Message
        from app.inbox.models.messages.message_link import MessageLink
        from app.inbox.services.messages.link_preview import (
            fetch_link_preview,
        )
        from app.inbox.serializers.message_serializer import (
            MessageSerializer,
        )

        print(
            f"🔗 BACKGROUND PREVIEW STARTED: "
            f"message={message_id} url={normalized_url}"
        )

        message = db.session.get(Message, message_id)

        if not message:
            print(
                f"🔗 BACKGROUND PREVIEW ABORTED: "
                f"message {message_id} no longer exists"
            )
            return

        try:
            preview_started = datetime.utcnow()

            preview = fetch_link_preview(normalized_url)

            preview_finished = datetime.utcnow()

            print(
                "🔗 BACKGROUND PREVIEW FETCH TIME:",
                (
                    preview_finished - preview_started
                ).total_seconds(),
                "seconds",
            )

            print("🔗 BACKGROUND PREVIEW:", preview)

            link = MessageLink.query.filter_by(
                message_id=message.id,
                normalized_url=normalized_url,
            ).first()

            if not link:
                print(
                    f"🔗 LINK PREVIEW ABORTED: "
                    f"link record missing for message={message.id}"
                )
                return

            link.title = preview.get("title")
            link.description = preview.get("description")
            link.image_url = preview.get("image_url")
            link.site_name = preview.get("site_name")
            link.domain = preview.get("domain")
            link.platform = preview.get("platform")
            link.content_type = preview.get("content_type")
            link.fetched_at = datetime.utcnow()

            db.session.commit()

            # Send the updated message to clients.
            db.session.refresh(message)

            serialized = MessageSerializer(message).to_dict()

            print(
                "🚨 ABOUT TO EMIT LINK PREVIEW",
                {
                    "message_id": message.id,
                    "conversation_id": message.conversation_id,
                    "room": f"conversation_{message.conversation_id}",
                },
                flush=True,
            )

            socketio.emit(
                "message:link_preview_ready",
                serialized,
                room=f"conversation_{message.conversation_id}",
            )

            print(
                "🚨 LINK PREVIEW EMIT COMPLETE",
                {
                    "message_id": message.id,
                    "conversation_id": message.conversation_id,
                },
                flush=True,
            )

            print(
                f"✅ BACKGROUND PREVIEW SAVED: "
                f"message={message.id}"
            )

        except Exception as exc:
            db.session.rollback()

            print(
                f"❌ BACKGROUND PREVIEW FAILED: "
                f"message={message_id} "
                f"url={raw_url} "
                f"error={exc}"
            )

            raise