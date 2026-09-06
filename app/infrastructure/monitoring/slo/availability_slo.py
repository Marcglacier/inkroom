# app/infrastructure/monitoring/slo/availability_slo.py


from app.infrastructure.monitoring.history.health_history import (
    HealthHistory,
)


class AvailabilitySLO:

    READY_STATUSES = {
        "healthy",
        "warning",
    }

    def __init__(
        self,
        history: HealthHistory,
        target_percentage: float = 99.9,
    ):

        self.history = history
        self.target_percentage = (
            target_percentage
        )

    def calculate(self) -> float:

        entries = self.history.get_history()

        total = len(entries)

        if total == 0:
            return 0.0

        available = sum(
            1
            for entry in entries
            if entry.get("status")
            in self.READY_STATUSES
        )

        return (
            available / total
        ) * 100

    def is_met(self) -> bool:

        return (
            self.calculate()
            >= self.target_percentage
        )

