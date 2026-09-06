# app/infrastructure/monitoring/checks/monitoring.py
import logging

from flask import Flask

from .health_monitor import HealthMonitor


logger = logging.getLogger(
    "inkroom.health"
)


health_monitor = None


def start_monitoring(app: Flask):

    global health_monitor

    if health_monitor is not None:

        logger.warning(
            "Health monitor already running"
        )

        return

    health_monitor = HealthMonitor(
        app=app,
        interval_seconds=30,
    )

    health_monitor.start()


def stop_monitoring():

    global health_monitor

    if health_monitor is None:
        return

    health_monitor.stop()

    health_monitor = None

def get_health_monitor():
    return health_monitor