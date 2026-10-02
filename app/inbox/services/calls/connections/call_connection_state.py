# app/inbox/services/calls/call_connection_state.py
from datetime import datetime


class CallConnectionState:
    def __init__(self):
        self._disconnected_at: dict[tuple[int, int], datetime] = {}

    def mark_disconnected(
        self,
        call_id: int,
        user_id: int,
    ) -> None:
        self._disconnected_at[(call_id, user_id)] = datetime.utcnow()

    def mark_reconnected(
        self,
        call_id: int,
        user_id: int,
    ) -> None:
        self._disconnected_at.pop((call_id, user_id), None)

    def clear(
        self,
        call_id: int,
    ) -> None:
        keys = [
            key
            for key in self._disconnected_at
            if key[0] == call_id
        ]
    
        for key in keys:
            self._disconnected_at.pop(key, None)    

    def disconnected_at(
        self,
        call_id: int,
        user_id: int,
    ) -> datetime | None:
        return self._disconnected_at.get((call_id, user_id))

    def disconnected_user_ids(self) -> set[int]:
        return {user_id for _, user_id in self._disconnected_at}

    def disconnected_calls(self) -> list[tuple[int, int, datetime]]:
        return [
            (call_id, user_id, disconnected_at)
            for (call_id, user_id), disconnected_at in self._disconnected_at.items()
        ]

call_connection_state = CallConnectionState()    