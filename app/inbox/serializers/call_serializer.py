# app/inbox/serializers/call_serializer.py

from app.common.serializers.base import SerializerMixin


class CallSerializer(SerializerMixin):

    def __init__(self, call):
        self.call = call

    def to_dict(self):
        return {
            "id": self.call.id,
            "conversation_id": self.call.conversation_id,
            "caller_id": self.call.caller_id,
            "receiver_id": self.call.receiver_id,
            "call_type": self.call.call_type,
            "status": self.call.status,

            "created_at": (
                self.call.created_at.isoformat() + "Z"
                if self.call.created_at
                else None
            ),

            "started_at": (
                self.call.started_at.isoformat() + "Z"
                if self.call.started_at
                else None
            ),

            "answered_at": (
                self.call.answered_at.isoformat() + "Z"
                if self.call.answered_at
                else None
            ),

            "ended_at": (
                self.call.ended_at.isoformat() + "Z"
                if self.call.ended_at
                else None
            ),
        }