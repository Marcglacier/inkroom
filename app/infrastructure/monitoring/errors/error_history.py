# app/infrastructure/monitoring/errors/error_history.py
class ErrorHistory:

    def __init__(self):
        self._errors = []

    def record(self, error: dict) -> None:

        self._errors.append(error)

    def get_errors(self) -> list[dict]:

        return list(self._errors)

    def latest(self) -> dict | None:

        if not self._errors:
            return None

        return self._errors[-1]

    def clear(self) -> None:

        self._errors.clear()