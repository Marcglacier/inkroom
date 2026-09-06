
from app.infrastructure.monitoring.errors import ErrorManager


def test_error_manager_can_be_created():

    manager = ErrorManager()

    assert manager is not None


def test_error_manager_records_error():

    manager = ErrorManager()

    error = {
        "type": "database",
        "message": "Database connection failed",
    }

    result = manager.record(error)

    assert result == error


def test_error_manager_stores_error():

    manager = ErrorManager()

    error = {
        "type": "database",
        "message": "Database connection failed",
    }

    manager.record(error)

    errors = manager.get_errors()

    assert errors == [error]


def test_error_manager_returns_latest_error():

    manager = ErrorManager()

    first = {
        "type": "database",
        "message": "Database connection failed",
    }

    second = {
        "type": "redis",
        "message": "Redis connection failed",
    }

    manager.record(first)
    manager.record(second)

    assert manager.latest() == second


def test_error_manager_returns_none_when_empty():

    manager = ErrorManager()

    assert manager.latest() is None


def test_error_manager_can_clear_errors():

    manager = ErrorManager()

    error = {
        "type": "database",
        "message": "Database connection failed",
    }

    manager.record(error)

    manager.clear()

    assert manager.get_errors() == []


def test_error_manager_preserves_multiple_errors():

    manager = ErrorManager()

    errors = [
        {
            "type": "database",
            "message": "Database failed",
        },
        {
            "type": "redis",
            "message": "Redis failed",
        },
        {
            "type": "storage",
            "message": "Storage failed",
        },
    ]

    for error in errors:
        manager.record(error)

    assert manager.get_errors() == errors

