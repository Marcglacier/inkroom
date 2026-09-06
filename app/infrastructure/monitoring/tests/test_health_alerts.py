from app.infrastructure.monitoring.alerts import HealthAlerts




def test_no_alert_when_health_is_healthy():

    alert = HealthAlerts.evaluate(
        {
            "status": "healthy",
        }
    )

    assert alert is None


def test_no_alert_when_health_is_warning():

    alert = HealthAlerts.evaluate(
        {
            "status": "warning",
        }
    )

    assert alert is None


def test_alert_when_health_is_critical():

    alert = HealthAlerts.evaluate(
        {
            "status": "critical",
        }
    )

    assert alert is not None
    assert alert["status"] == "critical"


def test_alert_when_health_is_unknown():

    alert = HealthAlerts.evaluate(
        {
            "status": "unknown",
        }
    )

    assert alert is not None
    assert alert["status"] == "unknown"


def test_alert_contains_message():

    alert = HealthAlerts.evaluate(
        {
            "status": "critical",
        }
    )

    assert "message" in alert
    assert alert["message"]


def test_alert_contains_original_result():

    health_result = {
        "status": "critical",
        "database": "critical",
        "capacity": {
            "status": "critical",
        },
    }

    alert = HealthAlerts.evaluate(
        health_result
    )

    assert alert["result"] == health_result