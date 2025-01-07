import json
import pytest

from cloudmailin.handlers import BaseHandler, CampaignClassifierHandler


# Assuming valid_email_payload.json exists in the test_data directory
@pytest.fixture
def valid_real_payload():
    """
    Load the valid email payload from the JSON test data file.
    """
    with open("tests/functional/test_data/valid_email_payload.json") as f:
        return json.load(f)


@pytest.mark.parametrize(
    "handler_class",
    [
        BaseHandler,  # Base handler
        CampaignClassifierHandler,  # Specialized handler
    ],
)
def test_email_processing_flow_with_handler(
    client, app, valid_real_payload, caplog, handler_class
):
    """
    Functional test to verify end-to-end email processing flow:
    - Valid payload is sent.
    - The correct handler processes the email.
    - Logs reflect the correct processing steps.
    - Email is 'stored' (via log placeholder for now).
    """
    with app.app_context():
        # Arrange
        handler_registry = app.config["handler_registry"]

        # Register the handler with a unique sender
        sender = "test_handler@example.com"
        handler_registry.register(sender, handler_class)

        caplog.clear()

        # Update the payload with the registered sender
        valid_real_payload["envelope"]["from"] = sender

        # Act
        # Send the payload
        response = client.post("/generic/new", json=valid_real_payload)

        # Assert: response
        assert (
            response.status_code == 200
        ), f"{handler_class.__name__} did not return 200 OK"

        # Assert: Log health check (check level and pattern)
        # Check dynamic log message
        assert any(
            record.levelname == "INFO"
            and f"[{handler_class.__name__}] Processing email" in record.message
            for record in caplog.records
        ), f"Expected log from handler {handler_class.__name__} not found"

        # Assert: Database Storage (temporary placeholder)
        assert any(
            record.levelname == "INFO" and "store in database" in record.message
            for record in caplog.records
        ), "Expected a log indicating database storage."

        # TODO: Replace database storage log assertion with an actual database check
