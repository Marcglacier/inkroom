
from app.infrastructure.monitoring.checks.health_monitor import (
    HealthMonitor,
    HealthService,
)
from app.infrastructure.monitoring.errors import (
    ErrorManager,
)


def test_health_monitor_records_health_service_error(
    app,
    monkeypatch,
):
    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    def failing_check(self):
        raise RuntimeError(
            "Database connection failed"
        )

    monkeypatch.setattr(
        HealthService,
        "check",
        failing_check,
    )

    monitor._check()

    errors = monitor.error_manager.get_errors()

    assert len(errors) == 1

    error = errors[0]

    assert error["error_type"] == "RuntimeError"
    assert (
        error["message"]
        == "Database connection failed"
    )


def test_health_monitor_keeps_health_check_running_after_error(
    app,
    monkeypatch,
):
    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    def failing_check(self):
        raise RuntimeError(
            "Temporary database failure"
        )

    monkeypatch.setattr(
        HealthService,
        "check",
        failing_check,
    )

    monitor._check()

    errors = monitor.get_errors()

    assert len(errors) == 1

    assert (
        errors[0]["message"]
        == "Temporary database failure"
    )

