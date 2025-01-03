import pytest
from unittest.mock import patch, Mock
from flask import Flask, current_app

from cloudmailin import create_app
from cloudmailin.handler_registry import HandlerRegistry
#from cloudmailin.generic import new_generic_email
from cloudmailin.schemas import Email

from icecream import ic


# --- Handler Registry Accesibility Tests --- #
def test_access_handler_registry_in_view():
    """
    Test that the handler registry can be accessed via app context.
    """
    app = create_app()
    with app.app_context():
        registry = current_app.config["handler_registry"]
        assert isinstance(registry, HandlerRegistry)


# --- Valid Request Tests --- #

def test_generic_view_selects_correct_handler(client, app, valid_email_data):
    """
    Test that the correct handler is selected based on the sender.
    """
    valid_email_data["envelope"]["from"] = "specific_sender@example.com"

    with app.app_context():
        handler_registry = current_app.config["handler_registry"]

        # Create a mock handler class with a 'handle' method
        MockHandler = type("MockHandler", (), {"handle": Mock()})

        handler_registry.register("specific_sender@example.com", MockHandler)

        # Spy on `get_handler_for_sender` to verify selection
        with patch.object(handler_registry, "get_handler_for_sender", wraps=handler_registry.get_handler_for_sender) as mock_get_handler:
            response = client.post("/generic/new", json=valid_email_data)
            
            # Assert the handler selection logic
            mock_get_handler.assert_called_once_with("specific_sender@example.com")

def test_generic_view_calls_handler_handle(client, app, valid_email_data):
    """
    Test that the selected handler's handle method is called with the Email object.
    """

    with app.app_context():
        handler_registry = app.config["handler_registry"]

        # Create a mock handler class with a 'handle' method
        MockHandler = type("MockHandler", (), {"handle": Mock()})
        handler_registry.register(valid_email_data["envelope"]["from"], MockHandler)

    response = client.post("/generic/new", json=valid_email_data)

    MockHandler.handle.assert_called_once()


def test_generic_view_valid_payload_returns_200_and_correct_json(client, valid_email_data):
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

# --- Handler error tetst --- #

#def test_generic_view_handler_exception(client, valid_flat_payload):
#    """
#    Test that an exception during handler execution returns a 500 error.
#    """
#    with patch("cloudmailin.generic.handler_registry") as mock_registry:
#        mock_handler = Mock()
#        mock_registry.get_handler_for_sender.return_value = mock_handler
#        mock_handler.handle.side_effect = Exception("Handler failure")
#
#        response = client.post("/generic/new", json=valid_flat_payload)
#
#        assert response.status_code == 500
#        data = response.get_json()
#        assert data["error"] == "Internal Server Error"


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
