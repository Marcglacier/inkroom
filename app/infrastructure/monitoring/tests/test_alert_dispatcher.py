from app.infrastructure.monitoring.alerts.alert_dispatcher import (
    AlertDispatcher,
)
from unittest.mock import patch
from app import create_app

from flask import Flask
from app.extensions import mail

def test_dispatcher_starts_empty():

    dispatcher = AlertDispatcher()

    assert dispatcher.get_dispatched() == []


def test_dispatcher_dispatches_alert():

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    result = dispatcher.dispatch(alert)

    assert result == alert
    assert dispatcher.get_dispatched() == [alert]


def test_dispatcher_keeps_multiple_alerts():

    dispatcher = AlertDispatcher()

    first_alert = {
        "status": "critical",
    }

    second_alert = {
        "status": "unknown",
    }

    dispatcher.dispatch(first_alert)
    dispatcher.dispatch(second_alert)

    assert dispatcher.get_dispatched() == [
        first_alert,
        second_alert,
    ]


def test_dispatcher_returns_latest_alert():

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
    }

    dispatcher.dispatch(alert)

    assert dispatcher.latest() == alert


def test_latest_returns_none_when_empty():

    dispatcher = AlertDispatcher()

    assert dispatcher.latest() is None


def test_dispatcher_returns_copy_of_alerts():

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
    }

    dispatcher.dispatch(alert)

    dispatched = dispatcher.get_dispatched()

    dispatched.clear()

    assert dispatcher.get_dispatched() == [alert]


def test_dispatcher_can_clear_alerts():

    dispatcher = AlertDispatcher()

    dispatcher.dispatch({
        "status": "critical",
    })

    dispatcher.clear()

    assert dispatcher.get_dispatched() == []
    assert dispatcher.latest() is None


def test_dispatcher_sends_health_alert_email(app):

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
        "result": {
            "status": "critical",
            "database": "unavailable",
        },
    }

    with app.app_context():

        with patch(
            "app.infrastructure.monitoring.alerts.alert_dispatcher.mail.send"
        ) as mock_send:

            dispatcher.dispatch(alert)

    mock_send.assert_called_once()

    message = mock_send.call_args[0][0]

    assert (
        message.subject
        == "InkRoom Health Alert: CRITICAL"
    )

    assert message.recipients == [
        app.config["MAIL_USERNAME"]
    ]

    assert (
        "Database is unavailable"
        in message.body
    )
def test_dispatcher_records_email_as_sent(
    app,
    monkeypatch,
):

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    sent = []

    def fake_send(message):
        sent.append(message)

    monkeypatch.setattr(
        "app.infrastructure.monitoring.alerts.alert_dispatcher.mail.send",
        fake_send,
    )

    with app.app_context():

        dispatcher.dispatch(alert)

    assert len(sent) == 1

def test_email_failure_does_not_break_dispatch(
    app,
    monkeypatch,
):

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    def failing_send(message):
        raise RuntimeError(
            "SMTP server unavailable"
        )

    monkeypatch.setattr(
        "app.infrastructure.monitoring.alerts.alert_dispatcher.mail.send",
        failing_send,
    )

    with app.app_context():

        result = dispatcher.dispatch(alert)

    assert result == alert

    assert (
        dispatcher.get_dispatched()
        == [alert]
    )

def test_dispatcher_records_successful_email_delivery(
    app,
    monkeypatch,
):

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    sent = []

    def fake_send(message):
        sent.append(message)

    monkeypatch.setattr(
        mail,
        "send",
        fake_send,
    )

    with app.app_context():

        dispatcher.dispatch(alert)

    deliveries = (
        dispatcher.get_delivery_history()
    )

    assert len(deliveries) == 1

    delivery = deliveries[0]

    assert delivery["alert"] == alert
    assert delivery["status"] == "sent"
    assert "timestamp" in delivery
    assert len(sent) == 1

def test_dispatcher_records_failed_email_delivery(
    app,
    monkeypatch,
):

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
    }

    def failing_send(message):
        raise RuntimeError(
            "SMTP server unavailable"
        )

    monkeypatch.setattr(
        mail,
        "send",
        failing_send,
    )

    with app.app_context():

        dispatcher.dispatch(alert)

    deliveries = (
        dispatcher.get_delivery_history()
    )

    assert len(deliveries) == 1

    delivery = deliveries[0]

    assert delivery["alert"] == alert
    assert delivery["status"] == "failed"
    assert delivery["error"] == (
        "SMTP server unavailable"
    )
    assert "timestamp" in delivery        

def test_dispatcher_returns_latest_delivery(
    app,
    monkeypatch,
):

    dispatcher = AlertDispatcher()

    monkeypatch.setattr(
        mail,
        "send",
        lambda message: None,
    )

    alert = {
        "status": "critical",
    }

    with app.app_context():

        dispatcher.dispatch(alert)

    latest = dispatcher.latest_delivery()

    assert latest is not None
    assert latest["status"] == "sent"
    assert latest["alert"] == alert

def test_dispatcher_clear_clears_delivery_history(
    app,
    monkeypatch,
):

    dispatcher = AlertDispatcher()

    monkeypatch.setattr(
        mail,
        "send",
        lambda message: None,
    )

    with app.app_context():

        dispatcher.dispatch({
            "status": "critical",
        })

    assert len(
        dispatcher.get_delivery_history()
    ) == 1

    dispatcher.clear()

    assert (
        dispatcher.get_delivery_history()
        == []
    )    

def test_email_failure_does_not_raise_exception():
    app = create_app()

    app.config["MAIL_USERNAME"] = "alerts@example.com"

    dispatcher = AlertDispatcher()

    alert = {
        "status": "critical",
        "message": "Database is unavailable",
        "result": {
            "status": "critical",
        },
    }

    with app.app_context():
        with patch(
            "app.infrastructure.monitoring.alerts.alert_dispatcher.mail.send",
            side_effect=Exception("SMTP connection failed"),
        ):
            result = dispatcher.dispatch(alert)

    assert result == alert

    delivery = (
        dispatcher.latest_delivery()
    )

    assert delivery is not None
    assert delivery["status"] == "failed"
    assert (
        delivery["error"]
        == "SMTP connection failed"
    )