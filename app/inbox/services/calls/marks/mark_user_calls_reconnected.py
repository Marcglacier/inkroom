# app/inbox/services/calls/mark_user_calls_reconnected.py
from app.inbox.services.calls.connections.call_connection_state import (
    call_connection_state,
)
from app.inbox.models import Call
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

class MarkUserCallsReconnected:

    def __init__(
        self,
        user_id: int,
    ):
        self.user_id = user_id

    def execute(self) -> None:

        for call_id, user_id, _ in (
            call_connection_state.disconnected_calls()
        ):
            if user_id != self.user_id:
                continue

            call = Call.query.get(call_id)

            if call is None:
                continue

            if BlockPolicy.blocks_either_user(
                call.caller_id,
                call.receiver_id,
            ):
                continue

            call_connection_state.mark_reconnected(
                call_id=call_id,
                user_id=user_id,
            )

            print(
                "📞 CALL RECONNECTED:",
                f"call={call_id}",
                f"user={user_id}",
            )