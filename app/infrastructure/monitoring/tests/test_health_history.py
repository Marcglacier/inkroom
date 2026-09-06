from app.infrastructure.monitoring.history.health_history import (
    HealthHistory,
)


def test_history_records_health_check():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    result = history.latest()

    assert result is not None
    assert result["status"] == "healthy"


def test_history_keeps_multiple_entries():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "warning",
        }
    )

    entries = history.get_history()

    assert len(entries) == 2
    assert entries[0]["status"] == "healthy"
    assert entries[1]["status"] == "warning"


def test_history_respects_max_entries():

    history = HealthHistory(
        max_entries=2
    )

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "warning",
        }
    )

    history.record(
        {
            "status": "critical",
        }
    )

    entries = history.get_history()

    assert len(entries) == 2
    assert entries[0]["status"] == "warning"
    assert entries[1]["status"] == "critical"

def test_history_summary_empty():

    history = HealthHistory()

    result = history.summary()

    assert result == {
        "total_checks": 0,
        "healthy": 0,
        "warning": 0,
        "critical": 0,
        "unknown": 0,
    }


def test_history_summary_all_healthy():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "healthy",
        }
    )

    result = history.summary()

    assert result["total_checks"] == 3
    assert result["healthy"] == 3
    assert result["warning"] == 0
    assert result["critical"] == 0
    assert result["unknown"] == 0


def test_history_summary_mixed_statuses():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "warning",
        }
    )

    history.record(
        {
            "status": "critical",
        }
    )

    history.record(
        {
            "status": "healthy",
        }
    )

    result = history.summary()

    assert result["total_checks"] == 4
    assert result["healthy"] == 2
    assert result["warning"] == 1
    assert result["critical"] == 1
    assert result["unknown"] == 0


def test_history_summary_unknown_status():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "something_weird",
        }
    )

    history.record(
        {}
    )

    result = history.summary()

    assert result["total_checks"] == 3
    assert result["healthy"] == 1
    assert result["warning"] == 0
    assert result["critical"] == 0
    assert result["unknown"] == 2

def test_history_reliability_counts_warning_as_ready():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "warning",
        }
    )

    history.record(
        {
            "status": "critical",
        }
    )

    history.record(
        {
            "status": "unknown",
        }
    )

    reliability = history.reliability()

    assert reliability == 50.0    

def test_history_reliability_is_100_when_all_checks_are_ready():

    history = HealthHistory()

    history.record(
        {
            "status": "healthy",
        }
    )

    history.record(
        {
            "status": "warning",
        }
    )

    history.record(
        {
            "status": "healthy",
        }
    )

    reliability = history.reliability()

    assert reliability == 100.0

def test_history_reliability_is_zero_when_no_checks_exist():

    history = HealthHistory()

    reliability = history.reliability()

    assert reliability == 0.0    

def test_history_summary_counts_statuses():

    history = HealthHistory()

    history.record({"status": "healthy"})
    history.record({"status": "healthy"})
    history.record({"status": "warning"})
    history.record({"status": "critical"})
    history.record({"status": "unknown"})

    summary = history.summary()

    assert summary["total_checks"] == 5
    assert summary["healthy"] == 2
    assert summary["warning"] == 1
    assert summary["critical"] == 1
    assert summary["unknown"] == 1


def test_history_summary_empty():

    history = HealthHistory()

    summary = history.summary()

    assert summary["total_checks"] == 0
    assert summary["healthy"] == 0
    assert summary["warning"] == 0
    assert summary["critical"] == 0
    assert summary["unknown"] == 0