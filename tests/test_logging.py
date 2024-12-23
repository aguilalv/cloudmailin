
import pytest
from unittest.mock import patch
from cloudmailin import create_app
import json
import logging
from cloudmailin.logging_setup import JSONFormatter


# --- Test Logging Initialization --- #

def test_logging_initialization():
    """
    Test that the app logs a startup message during initialization.
    """
    with patch("cloudmailin.__init__.Flask.logger") as mock_logger:
        app = create_app()
        mock_logger.info.assert_any_call("Application starting...")


# --- Test Incoming Request Logging --- #

def test_logging_incoming_request(client):
    """
    Test that incoming requests are logged with method and path.
    """
    with patch.object(client.application.logger, "info") as mock_logger:
        client.post("/generic/new", json={})
        mock_logger.assert_any_call("Received request: POST /generic/new")

# --- Test Logging Json format --- #

def test_json_logging_format(caplog):
    """
    Ensure that logs are formatted as JSON with required fields.
    """
    # Logger setup
    logger = logging.getLogger("test_json_logger")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    # Log capture
    with caplog.at_level(logging.INFO, logger="test_json_logger"):
        logger.info("Test JSON log message")

    # Validation
    assert len(caplog.records) > 0, "No logs were captured by caplog."
    log_record = caplog.records[-1]
    log_output = handler.format(log_record)  # Format the raw log record
    log_data = json.loads(log_output)

    assert log_data["level"] == "INFO"
    assert log_data["message"] == "Test JSON log message"
    assert "timestamp" in log_data
