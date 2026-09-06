# app/infrastructure/monitoring/errors/error_manager.py
from .error_history import ErrorHistory


class ErrorManager:

    def __init__(
        self,
        history: ErrorHistory | None = None,
    ):
        self.history = (
            history
            if history is not None
            else ErrorHistory()
        )

    def record(
        self,
        error: dict,
    ) -> dict:

        self.history.record(error)

        return error

    def get_errors(self) -> list[dict]:

        return self.history.get_errors()

    def latest(self) -> dict | None:

        return self.history.latest()

    def clear(self) -> None:

        self.history.clear()

