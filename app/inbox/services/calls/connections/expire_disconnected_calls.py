# app/inbox/services/calls/expire_disconnected_calls.py
from datetime import datetime, timedelta

from app.inbox.models import Call

from app.inbox.services.calls.connections.call_connection_state import (
    call_connection_state,
)
from app.inbox.services.calls.connections.find_active_calls_for_user import (
    FindActiveCallsForUser,
)


class ExpireDisconnectedCalls:
    GRACE_SECONDS = 30

    def execute(self) -> list[tuple[Call, int]]:    
        cutoff = datetime.utcnow() - timedelta(seconds=self.GRACE_SECONDS)
    
        expired = []
        
        for call in self._active_calls():
            disconnected_user_id = self._disconnected_user(call)
        
            if disconnected_user_id and self._should_expire(
                call,
                cutoff,
            ):
                expired.append((call, disconnected_user_id))
        
        return expired

    def _disconnected_user(self, call: Call) -> int | None:
        for user_id in (call.caller_id, call.receiver_id):
            if call_connection_state.disconnected_at(
                call.id,
                user_id,
            ):
                return user_id
    
        return None

    def _active_calls(self) -> list[Call]:
        calls: dict[int, Call] = {}

        for user_id in self._participant_ids():
            for call in FindActiveCallsForUser(user_id).execute():
                calls[call.id] = call

        return list(calls.values())

    def _participant_ids(self) -> set[int]:
        return call_connection_state.disconnected_user_ids()

    def _should_expire(
        self,
        call: Call,
        cutoff: datetime,
    ) -> bool:
        for user_id in (call.caller_id, call.receiver_id):
            disconnected_at = call_connection_state.disconnected_at(
                call.id,
                user_id,
            )

            if disconnected_at:
                
            
                if disconnected_at <= cutoff:
                    return True

        return False