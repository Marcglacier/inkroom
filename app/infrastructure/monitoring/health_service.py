# app/infrastructure/monitoring/health_service.py
from app.infrastructure.database.DatabaseHealthService.database_health import (
    DatabaseHealth,
)

from app.infrastructure.database.database_capacity_service import (
    DatabaseCapacityService,
)


class HealthService:

    def __init__(self):

        self.database_health = DatabaseHealth()
        self.database_capacity = (
            DatabaseCapacityService()
        )

    def check(self) -> dict:

        database_healthy = (
            self.database_health.check()
        )

        capacity = (
            self.database_capacity.check()
        )

        return {
            "status": (
                "healthy"
                if database_healthy
                else "unhealthy"
            ),
            "database": (
                "healthy"
                if database_healthy
                else "unhealthy"
            ),
            "capacity": capacity,
        }

    @staticmethod
    def is_ready(result: dict) -> bool:

        database_status = (
            result.get("database")
        )

        capacity = (
            result.get("capacity") or {}
        )

        capacity_status = (
            capacity.get("status")
        )

        if database_status != "healthy":
            return False

        if capacity_status in (
            "critical",
            "unknown",
        ):
            return False

        return True