# app/inbox/services/calls/find_active_calls_for_user.py
from app.inbox.constants.calls import CALL_STATUS_ACCEPTED
from app.inbox.models import Call


class FindActiveCallsForUser:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self) -> list[Call]:
        return Call.query.filter(
            Call.status == CALL_STATUS_ACCEPTED,
            (
                (Call.caller_id == self.user_id)
                | (Call.receiver_id == self.user_id)
            ),
        ).all()