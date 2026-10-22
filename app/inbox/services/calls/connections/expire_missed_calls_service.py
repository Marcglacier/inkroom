# app/inbox/services/calls/expire_missed_calls_service.py
from datetime import datetime, timedelta
from app.inbox.services.settings.blocks.block_policy import BlockPolicy
from app.extensions import db, socketio
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_CALLING,
    CALL_STATUS_RINGING,
    CALL_STATUS_MISSED,
)
from app.inbox.serializers.call_serializer import CallSerializer
from app.models.user import User
from app.sockets.calls.status import emit_call_status
from app.inbox.services.messages.create_system_message import (
    create_system_message,
)
from app.inbox.serializers.message_serializer import MessageSerializer

class ExpireMissedCallsService:

    DEADLINE_SECONDS = 30

    def execute(self) -> int:

        deadline = (
            datetime.utcnow()
            - timedelta(
                seconds=self.DEADLINE_SECONDS
            )
        )

        calls = (
            Call.query
            .filter(
                Call.status.in_(
                    [
                        CALL_STATUS_CALLING,
                        CALL_STATUS_RINGING,
                    ]
                ),
                Call.created_at <= deadline,
            )
            .all()
        )

        expired_count = 0

        for call in calls:
            is_blocked = BlockPolicy.blocks_either_user(
                call.caller_id,
                call.receiver_id,
            )

            call.status = CALL_STATUS_MISSED
            call.ended_at = datetime.utcnow()

            if is_blocked:
                expired_count += 1
                continue

            missed_message = create_system_message(
                conversation_id=call.conversation_id,
                sender_id=call.caller_id,
                event="missed_call",
                call_id=call.id,
                call_type=call.call_type,
            )

            socketio.emit(
                "message:new",
                MessageSerializer(missed_message).to_dict(),
                room=f"conversation_{call.conversation_id}",
            )

            caller = User.query.get(
                call.caller_id
            )

            if caller is None:
                continue

            payload = {
                "call": CallSerializer(
                    call
                ).to_dict(),
                "caller": {
                    "id": caller.id,
                    "username": caller.username,
                    "name": caller.name,
                    "avatar": caller.profile_picture,
                },
            }

            emit_call_status(
                socketio,
                call.caller_id,
                payload,
            )

            emit_call_status(
                socketio,
                call.receiver_id,
                payload,
            )

            expired_count += 1

        if expired_count:
            db.session.commit()

        return expired_count