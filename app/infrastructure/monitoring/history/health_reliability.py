# app/infrastructure/monitoring/history/health_reliability.py
class HealthReliability:

    READY_STATUSES = {
        "healthy",
        "warning",
    }

    @classmethod
    def calculate(
        cls,
        entries: list[dict],
    ) -> float:

        total = len(entries)

        if total == 0:
            return 0.0

        ready_checks = sum(
            1
            for entry in entries
            if entry.get("status") in cls.READY_STATUSES
        )

        return (
            ready_checks / total
        ) * 100