import pytest
from datetime import datetime
from cloudmailin.schemas import Email


# --- Shared Fixtures --- #


@pytest.fixture
def valid_nested_payload():
    """
    Provides a valid nested email payload for testing flatten_payload and preprocess_payload.
    """
    return {
        "envelope": {"from": "sender@example.com", "to": "recipient@example.com"},
        "headers": {
            "subject": "Test Subject",
            "date": "Mon, 16 Jan 2012 17:00:01 +0000",
        },
        "body": {
            "plain": "Test Plain Body.",
            "html": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
        },
    }


@pytest.fixture
def valid_flat_payload():
    """
    Provides a valid flat email payload for testing from_flat_data.
    """
    return {
        "sender": "sender@example.com",
        "recipient": "recipient@example.com",
        "subject": "Test Subject",
        "date": "Mon, 16 Jan 2012 17:00:01 +0000",
        "plain_body": "Test Plain Body.",
        "html_body": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
    }


# --- Static Method Tests: flatten_payload --- #


def test_flatten_payload_valid_input(valid_nested_payload):
    """
    Test flatten_payload with a well-structured nested email payload.

    Verifies that the method correctly extracts and flattens fields from
    nested structures.
    """
    expected_flat = {
        "sender": "sender@example.com",
        "recipient": "recipient@example.com",
        "subject": "Test Subject",
        "plain_body": "Test Plain Body.",
        "html_body": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
        "date": "Mon, 16 Jan 2012 17:00:01 +0000",
    }

    result = Email.flatten_payload(valid_nested_payload)
    assert result == expected_flat


@pytest.mark.parametrize(
    "missing_field, expected_key",
    [
        ("envelope.to", "recipient"),  # recipient maps to envelope.to
        ("headers.subject", "subject"),  # subject maps to headers.subject
        ("body.plain", "plain_body"),  # plain_body maps to body.plain
        ("body.html", "html_body"),  # html_body maps to body.html
        ("headers.date", "date"),  # date maps to headers.date
    ],
)
def test_flatten_payload_missing_fields(
    valid_nested_payload, missing_field, expected_key
):
    """
    Test flatten_payload with missing keys in the nested payload.

    Ensures that missing fields return None without raising errors.
    """
    # Navigate and remove the missing field
    keys = missing_field.split(".")
    target = valid_nested_payload
    for key in keys[:-1]:
        target = target.get(key, {})
    target.pop(keys[-1], None)

    result = Email.flatten_payload(valid_nested_payload)
    assert result[expected_key] is None


def test_flatten_payload_invalid_input():
    """
    Test flatten_payload with an invalid (non-dictionary) input.

    Ensures that the method raises a ValueError when input is not a dictionary.
    """
    with pytest.raises(ValueError, match="Input must be a dictionary"):
        Email.flatten_payload(["invalid", "structure"])


# --- Factory Method Tests: from_flat_data --- #


def test_from_flat_data_creates_valid_email(valid_flat_payload):
    """
    Test from_flat_data creates a valid Email instance.

    Ensures the factory method correctly initializes an Email model.
    """
    email = Email.from_flat_data(**valid_flat_payload)

    assert email.sender == "sender@example.com"
    assert email.recipient == "recipient@example.com"
    assert email.subject == "Test Subject"
    assert email.date == datetime.strptime(
        "Mon, 16 Jan 2012 17:00:01 +0000", "%a, %d %b %Y %H:%M:%S %z"
    )
    assert email.plain_body == "Test Plain Body."
    assert (
        email.html_body
        == '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>'
    )


# --- Preprocessing Tests: preprocess_payload --- #


def test_preprocess_payload_valid_input(valid_nested_payload):
    """
    Test preprocess_payload with valid nested payload.

    Verifies that preprocessing flattens the payload and parses the date correctly.
    """
    result = Email.preprocess_payload(valid_nested_payload)

    assert result["sender"] == "sender@example.com"
    assert result["recipient"] == "recipient@example.com"
    assert result["subject"] == "Test Subject"
    assert result["plain_body"] == "Test Plain Body."
    assert (
        result["html_body"]
        == '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>'
    )
    assert result["date"] == datetime.strptime(
        "Mon, 16 Jan 2012 17:00:01 +0000", "%a, %d %b %Y %H:%M:%S %z"
    )


@pytest.mark.parametrize(
    "missing_field, error_message",
    [
        ("envelope.from", "Missing required fields"),
        ("headers.subject", "Missing required fields"),
    ],
)
def test_preprocess_payload_missing_required_fields(
    valid_nested_payload, missing_field, error_message
):
    """
    Test preprocess_payload with missing required fields.

    Ensures that a ValueError is raised when required fields are missing.
    """
    keys = missing_field.split(".")
    target = valid_nested_payload
    for key in keys[:-1]:
        target = target.get(key, {})
    target.pop(keys[-1], None)

    with pytest.raises(ValueError, match=error_message):
        Email.preprocess_payload(valid_nested_payload)


def test_preprocess_payload_invalid_date(valid_nested_payload):
    """
    Test preprocess_payload with an invalid date format.

    Ensures that a ValueError is raised for an improperly formatted date.
    """
    valid_nested_payload["headers"]["date"] = "Invalid Date"

    with pytest.raises(ValueError, match="Invalid date format"):
        Email.preprocess_payload(valid_nested_payload)
