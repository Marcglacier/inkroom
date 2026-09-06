# app/infrastructure/monitoring/alerts/alert_manager.py

from .health_alerts import HealthAlerts
from app.infrastructure.monitoring.history import AlertHistory
from .alert_dispatcher import AlertDispatcher


class AlertManager:

    def __init__(
        self,
        history: AlertHistory | None = None,
        dispatcher: AlertDispatcher | None = None,
    ):
        self.history = (
            history
            if history is not None
            else AlertHistory()
        )

        self.dispatcher = (
            dispatcher
            if dispatcher is not None
            else AlertDispatcher()
        )

        # Tracks whether a health incident is
        # currently active.
        # Critical and unknown are treated as
        # the same incident.
        self._alert_active = False

    def process(
        self,
        health_result: dict,
    ) -> dict | None:

        alert = HealthAlerts.evaluate(
            health_result
        )

        # Healthy / warning / recovered state.
        # End the current alert incident.
        if alert is None:
            self._alert_active = False
            return None

        # Always preserve alert events in history.
        self.history.record(alert)

        # Suppress repeated emails while the same
        # health incident remains active.
        if self._alert_active:
            return alert

        # First alert in a new incident.
        self.dispatcher.dispatch(alert)

        self._alert_active = True

        return alert

    def get_alerts(self) -> list[dict]:

        return self.history.get_alerts()

    def latest(self) -> dict | None:

        return self.history.latest()

    def get_dispatched_alerts(
        self,
    ) -> list[dict]:

        return (
            self.dispatcher.get_dispatched()
        )

    def latest_dispatched_alert(
        self,
    ) -> dict | None:

        return self.dispatcher.latest()

    def clear(self) -> None:

        self.history.clear()
        self.dispatcher.clear()
        self._alert_active = False