# app/infrastructure/monitoring/alerts/health_alerts.py
class HealthAlerts:

    ALERT_STATUSES = {
        "critical",
        "unknown",
    }

    @classmethod
    def evaluate(
        cls,
        health_result: dict,
    ) -> dict | None:

        status = health_result.get(
            "status",
            "unknown",
        )

        if status not in cls.ALERT_STATUSES:
            return None

        if status == "critical":
            message = (
                "InkRoom health is critical"
            )
        else:
            message = (
                "InkRoom health status is unknown"
            )

        return {
            "status": status,
            "message": message,
            "result": health_result,
        }