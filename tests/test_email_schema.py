import pytest
from datetime import datetime
from pydantic import ValidationError
from cloudmailin.schemas import Email


# --- Factory Method Tests --- #


def test_from_flat_data_creates_valid_email():
    email = Email.from_flat_data(
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        date="Mon, 16 Jan 2012 17:00:01 +0000",
    )
    assert email.sender == "sender@example.com"
    assert email.recipient == "recipient@example.com"
    assert email.subject == "Test Subject"
    assert email.date == datetime.strptime(
        "Mon, 16 Jan 2012 17:00:01 +0000", "%a, %d %b %Y %H:%M:%S %z"
    )


def test_from_flat_data_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError):
        Email.from_flat_data(
            sender="invalid-email",
            recipient="recipient@example.com",
            subject="Test Subject",
            date="Mon, 16 Jan 2012 17:00:01 +0000",
        )


# --- Flattening payload Tests --- #


def test_email_flatten_payload_valid_structure():
    email_data = {
        "envelope": {"from": "sender@example.com", "to": "recipient@example.com"},
        "headers": {
            "subject": "Test Subject",
            "date": "Mon, 16 Jan 2012 17:00:01 +0000",
        },
    }
    email = Email(**email_data)
    assert email.sender == "sender@example.com"
    assert email.recipient == "recipient@example.com"
    assert email.subject == "Test Subject"


def test_email_flatten_payload_invalid_structure():
    with pytest.raises(ValidationError):
        Email(**{"invalid_key": "invalid_value"})
