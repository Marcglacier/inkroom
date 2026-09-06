# app/infrastructure/database/capacity/pool/pool_wait_status.py

class PoolWaitStatus:

    WARNING_THRESHOLD_MS = 100.0
    CRITICAL_THRESHOLD_MS = 500.0

    @classmethod
    def determine(
        cls,
        wait_time_ms: float | None,
    ) -> str:

        if wait_time_ms is None:
            return "unknown"

        if wait_time_ms >= cls.CRITICAL_THRESHOLD_MS:
            return "critical"

        if wait_time_ms >= cls.WARNING_THRESHOLD_MS:
            return "warning"

        return "healthy"

if __name__ == "__main__":

    print(PoolWaitStatus.determine(20))
    print(PoolWaitStatus.determine(150))
    print(PoolWaitStatus.determine(600))
    print(PoolWaitStatus.determine(None))    