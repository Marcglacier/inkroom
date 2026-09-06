from app.infrastructure.monitoring.errors import ErrorHistory


def test_error_history_starts_empty():

    history = ErrorHistory()

    assert history.get_errors() == []


def test_error_history_records_error():

    history = ErrorHistory()

    error = {
        "id": "error-1",
        "error_type": "DatabaseError",
        "message": "Database is unavailable",
    }

    history.record(error)

    assert history.get_errors() == [error]


def test_error_history_records_multiple_errors():

    history = ErrorHistory()

    first = {
        "id": "error-1",
        "error_type": "DatabaseError",
        "message": "Database is unavailable",
    }

    second = {
        "id": "error-2",
        "error_type": "TimeoutError",
        "message": "Request timed out",
    }

    history.record(first)
    history.record(second)

    assert history.get_errors() == [
        first,
        second,
    ]


def test_error_history_latest_returns_latest_error():

    history = ErrorHistory()

    first = {
        "id": "error-1",
        "error_type": "DatabaseError",
        "message": "Database is unavailable",
    }

    second = {
        "id": "error-2",
        "error_type": "TimeoutError",
        "message": "Request timed out",
    }

    history.record(first)
    history.record(second)

    assert history.latest() == second


def test_error_history_latest_returns_none_when_empty():

    history = ErrorHistory()

    assert history.latest() is None


def test_error_history_clear():

    history = ErrorHistory()

    error = {
        "id": "error-1",
        "error_type": "DatabaseError",
        "message": "Database is unavailable",
    }

    history.record(error)

    history.clear()

    assert history.get_errors() == []


def test_error_history_returns_copy():

    history = ErrorHistory()

    error = {
        "id": "error-1",
        "error_type": "DatabaseError",
        "message": "Database is unavailable",
    }

    history.record(error)

    errors = history.get_errors()

    errors.clear()

    assert history.get_errors() == [error]