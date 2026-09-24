# app/inbox/services/calls/media_switch_state.py
from threading import Lock


class MediaSwitchState:

    def __init__(self):
        self._requests = {}
        self._lock = Lock()

    def set(
        self,
        call_id: int,
        requested_type: str,
        requested_by: int,
    ) -> None:
        with self._lock:
            self._requests[call_id] = {
                "requested_type": requested_type,
                "requested_by": requested_by,
            }

    def exists(self, call_id: int) -> bool:
        with self._lock:
            return call_id in self._requests
        
    def get(self, call_id: int):
        with self._lock:
            return self._requests.get(
                call_id
            )    

    def clear(self, call_id: int) -> None:
        with self._lock:
            self._requests.pop(
                call_id,
                None,
            )

media_switch_state = MediaSwitchState()            