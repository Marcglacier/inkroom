# app/infrastructure/monitoring/checks/health_monitor.py

import logging
import threading

from flask import Flask

from ..health_service import HealthService

from app.infrastructure.monitoring.history.health_history import (
    HealthHistory,
)

from app.infrastructure.monitoring.history.health_reliability import (
    HealthReliability,
)
from app.infrastructure.monitoring.slo.availability_slo import (
    AvailabilitySLO,
)
from app.infrastructure.monitoring.alerts import (
    AlertManager,
)
from app.infrastructure.monitoring.errors import (
    ErrorManager,
)

logger = logging.getLogger(
    "inkroom.health"
)


class HealthMonitor:

    def __init__(
        self,
        app: Flask,
        interval_seconds: int = 30,
    ):

        self.app = app

        self.interval_seconds = (
            interval_seconds
        )

        self._stop_event = (
            threading.Event()
        )

        # Single source of historical health data
        self.history = HealthHistory()
        
        self.availability_slo = AvailabilitySLO(
            self.history
        )
        self.alert_manager = AlertManager()
        self.error_manager = ErrorManager()
  
        self._thread = None

    def start(self):

        if (
            self._thread
            and self._thread.is_alive()
        ):
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            name="inkroom-health-monitor",
            daemon=True,
        )

        self._thread.start()

        logger.info(
            "Health monitor started | "
            "interval=%ss",
            self.interval_seconds,
        )

    def stop(self):

        self._stop_event.set()

        logger.info(
            "Health monitor stopped"
        )

    def _run(self):

        while not self._stop_event.is_set():

            self._check()

            self._stop_event.wait(
                self.interval_seconds
            )

    def _check(self):

        try:

            with self.app.app_context():

                result = (
                    HealthService()
                    .check()
                )

                self.history.record( result )
                self.alert_manager.process( result )

            logger.info(
                "Health check completed | "
                "status=%s",
                result.get("status"),
            )

        except Exception as exc:

            logger.exception(
                "Automatic health check failed"
            )

            self.error_manager.record(
                {
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            
    def get_history(self):

        return self.history.get_history()

    def get_summary(self):

        return self.history.summary()

    def get_reliability(self):
        return HealthReliability.calculate(
        self.history.get_history()
    )

    def get_availability_slo(self):

        return {
            "availability": (
                self.availability_slo.calculate()
            ),
            "target": (
                self.availability_slo.target_percentage
            ),
            "met": (
                self.availability_slo.is_met()
            ),
        }

    def get_alerts(self):

        return self.alert_manager.get_alerts()


    def get_latest_alert(self):

        return self.alert_manager.latest()

    def get_errors(self):

        return self.error_manager.get_errors()