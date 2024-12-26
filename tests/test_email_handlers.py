
import pytest
from unittest.mock import patch
from cloudmailin.email_handlers import BaseHandler
from cloudmailin.schemas import Email

def test_base_handler_logs_health_message(valid_flat_payload, app):
    """
    Test that BaseHandler logs a health-related message when handling an email.
    """
    email = Email.from_flat_data(**valid_flat_payload)
    handler = BaseHandler()

    with patch.object(app.logger, "info") as mock_logger:
        handler.handle(email)
        mock_logger.assert_any_call("Processing email from sender@example.com")
