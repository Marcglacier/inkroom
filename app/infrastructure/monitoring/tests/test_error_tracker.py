from app.infrastructure.monitoring.errors import (
    ErrorTracker,
)


def test_error_tracker_records_error():

    tracker = ErrorTracker()

    error = tracker.record(
        error_type="DatabaseError",
        message="Database connection failed",
    )

    assert error is not None
    assert error["error_type"] == "DatabaseError"
    assert (
        error["message"]
        == "Database connection failed"
    )


def test_error_tracker_generates_error_id():

    tracker = ErrorTracker()

    error = tracker.record(
        error_type="DatabaseError",
        message="Database connection failed",
    )

    assert "id" in error
    assert error["id"]


def test_error_tracker_records_timestamp():

    tracker = ErrorTracker()

    error = tracker.record(
        error_type="DatabaseError",
        message="Database connection failed",
    )

    assert "timestamp" in error
    assert error["timestamp"]


def test_error_tracker_stores_multiple_errors():

    tracker = ErrorTracker()

    tracker.record(
        error_type="DatabaseError",
        message="Database failed",
    )

    tracker.record(
        error_type="RedisError",
        message="Redis failed",
    )

    errors = tracker.get_errors()

    assert len(errors) == 2


def test_error_tracker_returns_copy_of_errors():

    tracker = ErrorTracker()

    tracker.record(
        error_type="DatabaseError",
        message="Database failed",
    )

    errors = tracker.get_errors()

    errors.clear()

    assert len(tracker.get_errors()) == 1


def test_error_tracker_latest_returns_latest_error():

    tracker = ErrorTracker()

    tracker.record(
        error_type="DatabaseError",
        message="Database failed",
    )

    latest = tracker.record(
        error_type="RedisError",
        message="Redis failed",
    )

    assert tracker.latest() == latest


def test_error_tracker_latest_returns_none_when_empty():

    tracker = ErrorTracker()

    assert tracker.latest() is None


def test_error_tracker_clear():

    tracker = ErrorTracker()

    tracker.record(
        error_type="DatabaseError",
        message="Database failed",
    )

    tracker.clear()

    assert tracker.get_errors() == []
    assert tracker.latest() is None