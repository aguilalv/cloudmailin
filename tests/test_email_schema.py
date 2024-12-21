
import pytest
from pydantic import ValidationError
from cloudmailin.schemas import Email


# --- Factory Method Tests --- #

def test_from_flat_data_creates_valid_email():
    email = Email.from_flat_data(
        sender="john@example.com",
        recipient="recipient@example.com",
        subject="Test Subject"
    )
    assert email.sender == "john@example.com"
    assert email.recipient == "recipient@example.com"
    assert email.subject == "Test Subject"


def test_from_flat_data_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError):
        Email.from_flat_data(
            sender="invalid-email",
            recipient="recipient@example.com",
            subject="Test Subject"
        )


# --- Validator Logic Tests --- #

def test_email_flatten_payload_valid_structure():
    email_data = {
        "envelope": {"from": "john@example.com", "to": "recipient@example.com"},
        "headers": {"subject": "Flatten Test"}
    }
    email = Email(**email_data)
    assert email.sender == "john@example.com"
    assert email.recipient == "recipient@example.com"
    assert email.subject == "Flatten Test"


def test_email_flatten_payload_invalid_structure():
    with pytest.raises(ValidationError):
        Email(**{"invalid_key": "invalid_value"})
