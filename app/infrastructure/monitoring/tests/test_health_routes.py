from unittest.mock import patch
from app.infrastructure.monitoring.checks.health_monitor import (
    HealthMonitor,
)
from app import create_app


def make_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


def test_health_ready_healthy():

    with patch(
        "app.infrastructure.monitoring.health_routes.HealthService.check"
    ) as mock_check:

        mock_check.return_value = {
            "status": "healthy",
            "database": "healthy",
            "capacity": {
                "status": "healthy",
            },
        }

        app = make_app()
        client = app.test_client()

        response = client.get(
            "/api/health/ready"
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "ready"


def test_health_ready_warning():

    with patch(
        "app.infrastructure.monitoring.health_routes.HealthService.check"
    ) as mock_check:

        mock_check.return_value = {
            "status": "healthy",
            "database": "healthy",
            "capacity": {
                "status": "warning",
            },
        }

        app = make_app()
        client = app.test_client()

        response = client.get(
            "/api/health/ready"
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "ready"


def test_health_ready_critical():

    with patch(
        "app.infrastructure.monitoring.health_routes.HealthService.check"
    ) as mock_check:

        mock_check.return_value = {
            "status": "healthy",
            "database": "healthy",
            "capacity": {
                "status": "critical",
            },
        }

        app = make_app()
        client = app.test_client()

        response = client.get(
            "/api/health/ready"
        )

        assert response.status_code == 503

        data = response.get_json()

        assert data["status"] == "not_ready"


def test_health_ready_unknown():

    with patch(
        "app.infrastructure.monitoring.health_routes.HealthService.check"
    ) as mock_check:

        mock_check.return_value = {
            "status": "healthy",
            "database": "healthy",
            "capacity": {
                "status": "unknown",
            },
        }

        app = make_app()
        client = app.test_client()

        response = client.get(
            "/api/health/ready"
        )

        assert response.status_code == 503

        data = response.get_json()

        assert data["status"] == "not_ready"

def test_health_alerts_returns_recorded_alerts():
    app = make_app()

    with app.app_context():
        from app.infrastructure.monitoring.checks.health_monitor import (
            HealthMonitor,
        )

        monitor = HealthMonitor(app)

        monitor.alert_manager.process(
            {
                "status": "critical",
                "message": "Database is unavailable",
            }
        )

        with patch(
            "app.infrastructure.monitoring.monitoring_routes.get_health_monitor",
            return_value=monitor,
        ):
            client = app.test_client()

            response = client.get(
                "/api/alerts"
            )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 1
    assert len(data["alerts"]) == 1

    assert (
        data["alerts"][0]["status"]
        == "critical"
    )


def test_health_alerts_returns_empty_when_no_alerts():
    app = make_app()

    monitor = HealthMonitor(app)

    with patch(
        "app.infrastructure.monitoring.monitoring_routes.get_health_monitor",
        return_value=monitor,
    ):
        client = app.test_client()

        response = client.get(
            "/api/alerts"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 0
    assert data["alerts"] == []
def test_health_history_returns_recorded_history():
    app = make_app()

    monitor = HealthMonitor(app)

    monitor.history.record(
        {
            "status": "healthy",
            "database": "healthy",
            "capacity": {
                "status": "healthy",
            },
        }
    )

    with patch(
        "app.infrastructure.monitoring.monitoring_routes.get_health_monitor",
        return_value=monitor,
    ):
        client = app.test_client()

        response = client.get(
            "/api/health/history"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 1
    assert len(data["history"]) == 1
    assert data["history"][0]["status"] == "healthy"


def test_health_history_returns_empty_when_no_history():
    app = make_app()

    monitor = HealthMonitor(app)

    with patch(
        "app.infrastructure.monitoring.monitoring_routes.get_health_monitor",
        return_value=monitor,
    ):
        client = app.test_client()

        response = client.get(
            "/api/health/history"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 0
    assert data["history"] == []        