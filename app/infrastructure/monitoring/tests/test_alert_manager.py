from app.infrastructure.monitoring.alerts import (
    AlertManager, AlertDispatcher
)
from app.infrastructure.monitoring.history import (
    AlertHistory,
)

def test_manager_returns_no_alert_for_healthy():

    manager = AlertManager()

    result = manager.process(
        {
            "status": "healthy",
        }
    )

    assert result is None
    assert manager.get_alerts() == []


def test_manager_returns_no_alert_for_warning():

    manager = AlertManager()

    result = manager.process(
        {
            "status": "warning",
        }
    )

    assert result is None
    assert manager.get_alerts() == []


def test_manager_stores_critical_alert():

    manager = AlertManager()

    result = manager.process(
        {
            "status": "critical",
        }
    )

    assert result is not None
    assert result["status"] == "critical"

    alerts = manager.get_alerts()

    assert len(alerts) == 1
    assert alerts[0]["status"] == "critical"


def test_manager_stores_multiple_alerts():

    manager = AlertManager()

    manager.process(
        {
            "status": "critical",
        }
    )

    manager.process(
        {
            "status": "unknown",
        }
    )

    alerts = manager.get_alerts()

    assert len(alerts) == 2
    assert alerts[0]["status"] == "critical"
    assert alerts[1]["status"] == "unknown"


def test_manager_latest_returns_latest_alert():

    manager = AlertManager()

    manager.process(
        {
            "status": "critical",
        }
    )

    manager.process(
        {
            "status": "unknown",
        }
    )

    latest = manager.latest()

    assert latest is not None
    assert latest["status"] == "unknown"


def test_manager_latest_returns_none_when_empty():

    manager = AlertManager()

    assert manager.latest() is None


def test_manager_clear_removes_alerts():

    manager = AlertManager()

    manager.process(
        {
            "status": "critical",
        }
    )

    manager.process(
        {
            "status": "unknown",
        }
    )

    assert len(manager.get_alerts()) == 2

    manager.clear()

    assert manager.get_alerts() == []
    assert manager.latest() is None

def test_alert_manager_uses_alert_history():

    history = AlertHistory()

    manager = AlertManager(
        history=history
    )

    health_result = {
        "status": "critical",
    }

    manager.process(
        health_result
    )

    assert history.count() == 1
    assert history.latest() == manager.latest()


def test_alert_manager_does_not_record_non_alert():

    history = AlertHistory()

    manager = AlertManager(
        history=history
    )

    manager.process({
        "status": "healthy",
    })

    assert history.count() == 0    

def test_alert_manager_dispatches_critical_alert():

    dispatcher = AlertDispatcher()
    manager = AlertManager(
        dispatcher=dispatcher
    )

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    result = manager.process(alert)

    assert result["status"] == "critical"
    assert result["result"] == alert

    assert dispatcher.get_dispatched() == [result]


def test_alert_manager_does_not_dispatch_non_alert():

    dispatcher = AlertDispatcher()
    manager = AlertManager(
        dispatcher=dispatcher
    )

    result = manager.process(
        {
            "status": "healthy",
        }
    )

    assert result is None
    assert dispatcher.get_dispatched() == []

def test_same_alert_is_dispatched_only_once():
    dispatcher = AlertDispatcher()
    manager = AlertManager(
        dispatcher=dispatcher
    )

    critical_result = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    manager.process(critical_result)
    manager.process(critical_result)
    manager.process(critical_result)

    dispatched = (
        manager.get_dispatched_alerts()
    )

    assert len(dispatched) == 1  

def test_alert_is_dispatched_again_after_recovery():
    dispatcher = AlertDispatcher()
    manager = AlertManager(
        dispatcher=dispatcher
    )

    critical_result = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    healthy_result = {
        "status": "healthy",
        "database": "healthy",
    }

    manager.process(critical_result)

    manager.process(critical_result)

    manager.process(healthy_result)

    manager.process(critical_result)

    dispatched = (
        manager.get_dispatched_alerts()
    )

    assert len(dispatched) == 2

def test_different_alert_states_in_same_incident_are_dispatched_once():
    dispatcher = AlertDispatcher()
    manager = AlertManager(
        dispatcher=dispatcher
    )

    critical_result = {
        "status": "critical",
    }

    unknown_result = {
        "status": "unknown",
    }

    manager.process(critical_result)
    manager.process(unknown_result)

    dispatched = (
        manager.get_dispatched_alerts()
    )

    assert len(dispatched) == 1
    assert dispatched[0]["status"] == "critical"

def test_alert_incident_resets_after_recovery():
    dispatcher = AlertDispatcher()

    manager = AlertManager(
        dispatcher=dispatcher
    )

    critical_result = {
        "status": "critical",
    }

    unknown_result = {
        "status": "unknown",
    }

    healthy_result = {
        "status": "healthy",
    }

    # First incident starts.
    manager.process(critical_result)

    # Same incident changes status.
    manager.process(unknown_result)

    # Recovery ends the incident.
    manager.process(healthy_result)

    # A genuinely new incident starts.
    manager.process(critical_result)

    dispatched = (
        manager.get_dispatched_alerts()
    )

    assert len(dispatched) == 2

    assert (
        dispatched[0]["status"]
        == "critical"
    )

    assert (
        dispatched[1]["status"]
        == "critical"
    )    