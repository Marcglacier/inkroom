# app/infrastructure/database/capacity/capacity_status.py


class CapacityStatus:

    WARNING_THRESHOLD = 0.70
    CRITICAL_THRESHOLD = 0.85

    @classmethod
    def determine(
        cls,
        *utilizations: float | None,
        pool_wait_status: str | None = None,
    ) -> str:

        if pool_wait_status == "critical":
            return "critical"

        valid_utilizations = [
            value
            for value in utilizations
            if value is not None
        ]

        if not valid_utilizations:
            if pool_wait_status == "warning":
                return "warning"

            return "unknown"

        worst_utilization = max(
            valid_utilizations
        )

        if (
            worst_utilization
            >= cls.CRITICAL_THRESHOLD
        ):
            return "critical"

        if (
            worst_utilization
            >= cls.WARNING_THRESHOLD
        ):
            return "warning"

        if pool_wait_status == "warning":
            return "warning"

        return "healthy"