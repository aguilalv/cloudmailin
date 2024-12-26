
import pytest
from unittest.mock import patch
from cloudmailin.email_handlers import BaseHandler
from cloudmailin.schemas import Email

### OLD - TO DELETE? ###

from cloudmailin.email_handlers import EmailHandler


def test_generic_handler_returns_email_unchanged():
    # Arrange: Create an Email object using the factory method
    email = Email.from_flat_data(
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        date="Mon, 16 Jan 2012 17:00:01 +0000",
        plain="Test Plain Body.",
        html='<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
    )

    # Act: Process the Email object with the generic handler
    handler = EmailHandler()
    result = handler.handle(email)

    # Assert: The result should match the input Email object
    assert result == email

### END OLD ###


def test_base_handler_logs_health_message(valid_flat_payload, app):
    """
    Test that BaseHandler logs a health-related message when handling an email.
    """
    email = Email.from_flat_data(**valid_flat_payload)
    handler = BaseHandler()

    with patch.object(app.logger, "info") as mock_logger:
        handler.handle(email)
        mock_logger.assert_any_call("Processing email from sender@example.com")
