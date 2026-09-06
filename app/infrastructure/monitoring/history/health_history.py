# app/infrastructure/monitoring/history/health_history.py

from collections import deque
from datetime import datetime, timezone
from .health_reliability import HealthReliability

class HealthHistory:

    def __init__(self, max_entries: int = 100):

        self.entries = deque(
            maxlen=max_entries
        )

    def record(
        self,
        result: dict,
    ) -> None:

        self.entries.append(
            {
                "timestamp": (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                ),
                "status": result.get(
                    "status",
                    "unknown",
                ),
                "result": result,
            }
        )

    def get_history(self) -> list[dict]:

        return list(self.entries)

    def latest(self) -> dict | None:

        if not self.entries:
            return None

        return self.entries[-1]

    def summary(self) -> dict:

        total = len(self.entries)

        if total == 0:
            return {
                "total_checks": 0,
                "healthy": 0,
                "warning": 0,
                "critical": 0,
                "unknown": 0,
            }

        counts = {
            "healthy": 0,
            "warning": 0,
            "critical": 0,
            "unknown": 0,
        }

        for entry in self.entries:

            status = entry.get(
                "status",
                "unknown",
            )

            if status not in counts:
                status = "unknown"

            counts[status] += 1

        return {
            "total_checks": total,
            **counts,
        }

    def reliability(self) -> float:

        return HealthReliability.calculate(
            self.get_history()
        )