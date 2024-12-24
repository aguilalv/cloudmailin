import pytest


# --- Shared Fixture for Valid Email Data --- #


@pytest.fixture
def valid_email_data():
    """
    Provides a valid generic email payload for tests.
    """
    return {
        "envelope": {"from": "sender@example.com", "to": "recipient@example.com"},
        "headers": {
            "subject": "Test Subject",
            "date": "Mon, 16 Jan 2012 17:00:01 +0000",
        },
        "plain": "Test Plain Body.",
        "html": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
    }


# --- Valid Request Tests --- #


def test_generic_view_valid_payload(client, valid_email_data):
    """
    Test /generic/new with a valid payload.

    Ensures that a valid payload returns a 200 OK status
    and the correct JSON response.
    """
    response = client.post("/generic/new", json=valid_email_data)

    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "sender": "sender@example.com",
        "recipient": "recipient@example.com",
        "subject": "Test Subject",
        "date": "Mon, 16 Jan 2012 17:00:01 GMT",
        "plain": "Test Plain Body.",
        "html": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
    }


# --- Invalid Input Tests --- #


@pytest.mark.parametrize(
    "field, value, error_message",
    [
        ("envelope.from", "invalid-email", "Validation failed"),  # Invalid sender email
        ("headers.date", "Invalid Date", "Validation failed"),  # Invalid date format
    ],
)
def test_generic_view_invalid_input(
    client, valid_email_data, field, value, error_message
):
    """
    Parametrized test for invalid input values.

    Ensures specific fields with invalid data return a 400 error.
    """
    keys = field.split(".")
    target = valid_email_data
    for key in keys[:-1]:
        target = target.get(key, {})
    target[keys[-1]] = value

    response = client.post("/generic/new", json=valid_email_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert error_message in data["error"]


# --- Missing Required Fields Tests --- #


@pytest.mark.parametrize(
    "missing_field, error_message",
    [
        ("headers.subject", "Validation failed"),  # Missing subject
        ("envelope.from", "Validation failed"),  # Missing sender
    ],
)
def test_generic_view_missing_required_fields(
    client, valid_email_data, missing_field, error_message
):
    """
    Parametrized test for missing required fields.

    Ensures that missing required fields return a 400 error.
    """
    keys = missing_field.split(".")
    target = valid_email_data
    for key in keys[:-1]:
        target = target.get(key, {})
    target.pop(keys[-1], None)

    response = client.post("/generic/new", json=valid_email_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert error_message in data["error"]
