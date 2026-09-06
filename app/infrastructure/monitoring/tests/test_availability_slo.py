
from app.infrastructure.monitoring.history.health_history import (
    HealthHistory,
)

from app.infrastructure.monitoring.slo.availability_slo import (
    AvailabilitySLO,
)


def test_availability_slo_reads_health_history():

    history = HealthHistory()

    history.record({"status": "healthy"})
    history.record({"status": "warning"})
    history.record({"status": "critical"})

    slo = AvailabilitySLO(history)

    assert slo.calculate() == 66.66666666666666


def test_availability_slo_counts_warning_as_available():

    history = HealthHistory()

    history.record({"status": "warning"})
    history.record({"status": "warning"})

    slo = AvailabilitySLO(history)

    assert slo.calculate() == 100.0


def test_availability_slo_counts_critical_as_unavailable():

    history = HealthHistory()

    history.record({"status": "healthy"})
    history.record({"status": "critical"})

    slo = AvailabilitySLO(history)

    assert slo.calculate() == 50.0


def test_availability_slo_counts_unknown_as_unavailable():

    history = HealthHistory()

    history.record({"status": "healthy"})
    history.record({"status": "unknown"})

    slo = AvailabilitySLO(history)

    assert slo.calculate() == 50.0


def test_availability_slo_empty_history():

    history = HealthHistory()

    slo = AvailabilitySLO(history)

    assert slo.calculate() == 0.0


def test_availability_slo_target_is_met():

    history = HealthHistory()

    history.record({"status": "healthy"})
    history.record({"status": "healthy"})
    history.record({"status": "warning"})

    slo = AvailabilitySLO(
        history,
        target_percentage=99.9,
    )

    assert slo.is_met() is True


def test_availability_slo_target_is_not_met():

    history = HealthHistory()

    history.record({"status": "healthy"})
    history.record({"status": "critical"})

    slo = AvailabilitySLO(
        history,
        target_percentage=99.9,
    )

    assert slo.is_met() is False

