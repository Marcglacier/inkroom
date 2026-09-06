# app/infrastructure/monitoring/errors/error_tracker.py
from datetime import datetime, timezone
from uuid import uuid4


class ErrorTracker:

    def __init__(self):

        self.errors = []

    def record(
        self,
        error_type: str,
        message: str,
    ) -> dict:

        error = {
            "id": str(uuid4()),
            "error_type": error_type,
            "message": message,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        self.errors.append(error)

        return error

    def get_errors(self) -> list[dict]:

        return list(self.errors)

    def latest(self) -> dict | None:

        if not self.errors:
            return None

        return self.errors[-1]

    def clear(self) -> None:

        self.errors.clear()