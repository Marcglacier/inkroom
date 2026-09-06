from unittest.mock import patch
import pytest
from app.infrastructure.monitoring.checks.health_monitor import (
    HealthMonitor,
)


def test_health_monitor_records_check(app):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    health_result = {
        "status": "healthy",
        "database": "healthy",
        "capacity": {
            "status": "healthy",
        },
    }

    with patch(
        "app.infrastructure.monitoring.checks.health_monitor.HealthService.check",
        return_value=health_result,
    ):

        monitor._check()

    latest = monitor.history.latest()

    assert latest is not None
    assert latest["status"] == "healthy"
    assert latest["result"] == health_result


def test_health_monitor_records_warning(app):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    health_result = {
        "status": "healthy",
        "database": "healthy",
        "capacity": {
            "status": "warning",
        },
    }

    with patch(
        "app.infrastructure.monitoring.checks.health_monitor.HealthService.check",
        return_value=health_result,
    ):

        monitor._check()

    latest = monitor.history.latest()

    assert latest is not None
    assert latest["status"] == "healthy"
    assert latest["result"]["capacity"]["status"] == "warning"

def test_health_monitor_exposes_history(app):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    health_result = {
        "status": "healthy",
        "database": "healthy",
        "capacity": {
            "status": "healthy",
        },
    }

    with patch(
        "app.infrastructure.monitoring.checks.health_monitor.HealthService.check",
        return_value=health_result,
    ):

        monitor._check()

    history = monitor.get_history()

    assert len(history) == 1
    assert history[0]["status"] == "healthy"


def test_health_monitor_calculates_reliability(app):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    monitor.history.record(
        {
            "status": "healthy",
        }
    )

    monitor.history.record(
        {
            "status": "warning",
        }
    )

    monitor.history.record(
        {
            "status": "critical",
        }
    )

    reliability = (
        monitor.get_reliability()
    )

    assert reliability == pytest.approx(
        66.66666666666666
    ) 

def test_health_monitor_exposes_availability_slo(app):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    assert monitor.availability_slo is not None
    assert (
        monitor.availability_slo.history
        is monitor.history
    )

def test_health_monitor_records_critical_alert(app):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    health_result = {
        "status": "critical",
        "database": "critical",
        "capacity": {
            "status": "critical",
        },
    }

    with patch(
        "app.infrastructure.monitoring.checks.health_monitor.HealthService.check",
        return_value=health_result,
    ):

        monitor._check()

    latest_alert = (
        monitor.get_latest_alert()
    )

    assert latest_alert is not None
    assert latest_alert["status"] == "critical"
    assert (
        latest_alert["result"]
        == health_result
    )    

       