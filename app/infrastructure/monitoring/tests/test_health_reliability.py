from app.infrastructure.monitoring.history.health_reliability import (
    HealthReliability,
)


def test_reliability_all_healthy():

    entries = [
        {"status": "healthy"},
        {"status": "healthy"},
        {"status": "healthy"},
    ]

    result = HealthReliability.calculate(entries)

    assert result == 100.0


def test_reliability_warning_is_still_ready():

    entries = [
        {"status": "healthy"},
        {"status": "warning"},
        {"status": "healthy"},
    ]

    result = HealthReliability.calculate(entries)

    assert result == 100.0


def test_reliability_critical_reduces_reliability():

    entries = [
        {"status": "healthy"},
        {"status": "healthy"},
        {"status": "critical"},
        {"status": "healthy"},
    ]

    result = HealthReliability.calculate(entries)

    assert result == 75.0


def test_reliability_unknown_reduces_reliability():

    entries = [
        {"status": "healthy"},
        {"status": "unknown"},
        {"status": "healthy"},
        {"status": "healthy"},
    ]

    result = HealthReliability.calculate(entries)

    assert result == 75.0


def test_reliability_mixed_statuses():

    entries = [
        {"status": "healthy"},
        {"status": "warning"},
        {"status": "critical"},
        {"status": "unknown"},
        {"status": "healthy"},
    ]

    result = HealthReliability.calculate(entries)

    assert result == 60.0


def test_reliability_empty_history():

    entries = []

    result = HealthReliability.calculate(entries)

    assert result == 0.0


def test_reliability_unknown_status_counts_as_not_ready():

    entries = [
        {"status": "healthy"},
        {"status": "something_weird"},
        {"status": "healthy"},
        {"status": "warning"},
    ]

    result = HealthReliability.calculate(entries)

    assert result == 75.0