# app/inbox/services/calls/mark_call_connection_disconnected.py
from app.inbox.models import Call
from app.inbox.services.calls.connections.call_connection_state import (
    call_connection_state,
)
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

class MarkCallConnectionDisconnected:
    def __init__(
        self,
        call_id: int,
        user_id: int,
    ):
        self.call_id = call_id
        self.user_id = user_id

    def execute(self) -> None:
        call = Call.query.get(self.call_id)

        if call is None:
            return

        if self.user_id not in (
            call.caller_id,
            call.receiver_id,
        ):
            return

        if BlockPolicy.blocks_either_user(
            call.caller_id,
            call.receiver_id,
        ):
            return

        if call.status != "accepted":
            return

        call_connection_state.mark_disconnected(
            call_id=call.id,
            user_id=self.user_id,
        )

        print(
            "📞 CALL CONNECTION LOST:",
            f"call={call.id}",
            f"user={self.user_id}",
        )