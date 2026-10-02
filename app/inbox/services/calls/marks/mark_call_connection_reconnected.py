# app/inbox/services/calls/marks/mark_call_connection_reconnected.py
from app.inbox.models import Call
from app.inbox.services.calls.connections.call_connection_state import (
    call_connection_state,
)


class MarkCallConnectionReconnected:
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

        call_connection_state.mark_reconnected(
            call_id=call.id,
            user_id=self.user_id,
        )

        print(
            "📞 CALL CONNECTION RESTORED:",
            f"call={call.id}",
            f"user={self.user_id}",
        )