# app/infrastructure/monitoring/history/alert_history.py
class AlertHistory:

    def __init__(self):
        self._alerts = []

    def record(self, alert: dict) -> dict:
        self._alerts.append(alert)

        return alert

    def get_alerts(self) -> list[dict]:
        return list(self._alerts)

    def latest(self) -> dict | None:

        if not self._alerts:
            return None

        return self._alerts[-1]

    def count(self) -> int:
        return len(self._alerts)

    def clear(self) -> None:
        self._alerts.clear()