# from pathlib import Path
# import tempfile

from unittest.mock import patch
import pytest
import textwrap

from cloudmailin import create_app

# test_db_file = Path(__file__) / "data.sql"
# with open(test_db_file)


# Configure standard hook in pytest to pass personalised command line arguments
def pytest_addoption(parser):
    parser.addoption(
        "--base-url",  # The name of the argument
        action="store",  # Tells pytest to store the value provided with the argument
        default="http://localhost:5000",  # Default value when the argument is not provided
        help="Base URL for the test environment",  # Description shown in help
    )


# Fixture that gets auto-applied to all tests in this file
# Mocks the firestore client to isolate these unit tests
# from the actual service (e.g. avoids need for credentials)
@pytest.fixture(autouse=True)
def mock_firestore_client():
    """
    Automatically mock the Firestore client for all tests.
    """
    with patch("cloudmailin.db.firestore.Client") as mock_client:
        yield mock_client


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture
def app():
    #    db_fd, db_path = tempfile.mkstemp(

    app = create_app({"TESTING": True})
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# --- Data Fixtures --- #


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
        "plain": "Test Plain Body.",
        "html": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
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
        "plain": "Test Plain Body.",
        "html": '<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
    }


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


# --- Fixture: Valid Handlers and Steps Configuration --- #


@pytest.fixture
def valid_yaml_config():
    """
    Provides a valid YAML configuration for handlers and steps.
    """
    return textwrap.dedent(
        """
    handlers:
      CampaignClassifierHandler:
        steps:
          - cloudmailin.handlers.steps.assign_campaign_type
        senders:
          - "newsletter@example.com"
          - "promo@example.com"
    """
    )
