# app/inbox/services/calls/mark_user_calls_disconnected.py
from app.inbox.services.calls.connections.call_connection_state import call_connection_state
from app.inbox.services.calls.connections.find_active_calls_for_user import FindActiveCallsForUser
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

class MarkUserCallsDisconnected:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self) -> None:
        calls = FindActiveCallsForUser(self.user_id).execute()

        for call in calls:
            if BlockPolicy.blocks_either_user(
                call.caller_id,
                call.receiver_id,
            ):
                continue

            call_connection_state.mark_disconnected(
                call_id=call.id,
                user_id=self.user_id,
            )
            print(
                "📞 CALL DISCONNECTED:",
                f"call={call.id}",
                f"user={self.user_id}",
            )