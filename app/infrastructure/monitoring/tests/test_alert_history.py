from app.infrastructure.monitoring.history import (
    AlertHistory,
)


def test_alert_history_starts_empty():

    history = AlertHistory()

    assert history.get_alerts() == []
    assert history.latest() is None
    assert history.count() == 0


def test_alert_history_records_alert():

    history = AlertHistory()

    alert = {
        "status": "critical",
        "message": "Database unavailable",
    }

    history.record(alert)

    assert history.count() == 1
    assert history.latest() == alert


def test_alert_history_records_multiple_alerts():

    history = AlertHistory()

    first = {
        "status": "critical",
    }

    second = {
        "status": "unknown",
    }

    history.record(first)
    history.record(second)

    assert history.count() == 2
    assert history.latest() == second


def test_alert_history_returns_copy():

    history = AlertHistory()

    alert = {
        "status": "critical",
    }

    history.record(alert)

    alerts = history.get_alerts()

    alerts.clear()

    assert history.count() == 1


def test_alert_history_clear():

    history = AlertHistory()

    history.record({
        "status": "critical",
    })

    history.clear()

    assert history.get_alerts() == []
    assert history.latest() is None
    assert history.count() == 0