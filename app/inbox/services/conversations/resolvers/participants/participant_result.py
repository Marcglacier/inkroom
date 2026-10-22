#participant_result.py
from dataclasses import dataclass


@dataclass(slots=True)
class ParticipantResult:
    other_user_id: int
    username: str
    name: str
    avatar: str | None
    is_saved_messages: bool
    is_deleted: bool = False
    is_blocked: bool = False
    is_blocker: bool = False