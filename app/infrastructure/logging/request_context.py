# app/infrastructure/logging/request_context.py

from contextvars import ContextVar
from uuid import uuid4


_request_id: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


def generate_request_id() -> str:
    return uuid4().hex


def set_request_id(request_id: str) -> None:
    _request_id.set(request_id)


def get_request_id() -> str | None:
    return _request_id.get()


def clear_request_id() -> None:
    _request_id.set(None)