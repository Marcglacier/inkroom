from app.infrastructure.monitoring.health_service import HealthService


def test_healthy_is_ready():

    result = {
        "database": "healthy",
        "capacity": {
            "status": "healthy"
        },
    }

    assert HealthService.is_ready(result) is True


def test_warning_is_ready():

    result = {
        "database": "healthy",
        "capacity": {
            "status": "warning"
        },
    }

    assert HealthService.is_ready(result) is True


def test_critical_is_not_ready():

    result = {
        "database": "healthy",
        "capacity": {
            "status": "critical"
        },
    }

    assert HealthService.is_ready(result) is False


def test_unknown_is_not_ready():

    result = {
        "database": "healthy",
        "capacity": {
            "status": "unknown"
        },
    }

    assert HealthService.is_ready(result) is False


def test_unhealthy_database_is_not_ready():

    result = {
        "database": "unhealthy",
        "capacity": {
            "status": "healthy"
        },
    }

    assert HealthService.is_ready(result) is False