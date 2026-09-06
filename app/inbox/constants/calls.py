# app/inbox/constants/calls.py

# ============================================================
# CALL TYPES
# ============================================================

CALL_TYPE_AUDIO = "audio"
CALL_TYPE_VIDEO = "video"


# ============================================================
# CALL STATUS
# ============================================================

# The caller has initiated the call, but the recipient's
# client has not yet been reached.
CALL_STATUS_CALLING = "calling"

# The recipient has been reached and is being notified
# of the incoming call.
CALL_STATUS_RINGING = "ringing"

CALL_STATUS_ACCEPTED = "accepted"

CALL_STATUS_DECLINED = "declined"

CALL_STATUS_MISSED = "missed"

CALL_STATUS_ENDED = "ended"

CALL_STATUS_CANCELLED = "cancelled"

CALL_STATUS_BUSY = "busy"