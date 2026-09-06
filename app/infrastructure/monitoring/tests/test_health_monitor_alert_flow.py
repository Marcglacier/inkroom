
from unittest.mock import patch

from app.infrastructure.monitoring.checks.health_monitor import (
    HealthMonitor,
    HealthService,
)


def test_health_monitor_creates_and_dispatches_alert(
    app,
    monkeypatch,
):

    monitor = HealthMonitor(
        app,
        interval_seconds=30,
    )

    health_result = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    monkeypatch.setattr(
        HealthService,
        "check",
        lambda self: health_result,
    )

    with patch(
        "app.infrastructure.monitoring.alerts.alert_dispatcher.mail.send"
    ) as mock_send:

        monitor._check()

    alerts = monitor.get_alerts()

    assert len(alerts) == 1
    assert alerts[0]["status"] == "critical"

    dispatched = (
        monitor.alert_manager
        .get_dispatched_alerts()
    )

    assert len(dispatched) == 1
    assert dispatched[0]["status"] == "critical"

    # Health alert reached the email dispatcher
    mock_send.assert_called_once()

    email = mock_send.call_args[0][0]

    assert (
        email.subject
        == "InkRoom Health Alert: CRITICAL"
    )

    assert (
        "Database is unavailable"
        in email.body
    )

