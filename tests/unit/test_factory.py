from unittest.mock import mock_open, patch
from cloudmailin.handler_registry import HandlerRegistry
from cloudmailin import create_app
from textwrap import dedent
import os

# from cloudmailin.config_loader import initialize_handler_registry_from_config


def test_create_app_initializes_handler_registry_correctly():
    """
    Test that create_app correctly initializes handler_registry with configuration.
    """
    mock_registry = HandlerRegistry()

    # Patch the reference in __init__.py
    with patch(
        "cloudmailin.handler_registry.initialize_handler_registry_from_config"
    ) as mock_init:
        mock_init.return_value = mock_registry

        # Create the app
        app = create_app()

        # Verify the function was called with the expected configuration path
        mock_init.assert_called_once_with("config/handler_config.yaml")

        # Verify the registry in the app is the mocked registry
        assert (
            app.config["handler_registry"] is mock_registry
        ), "The handler_registry in app.config is not the mocked registry."


# def test_create_app_testing_flag_only_on_when_initialized():
#     assert not create_app().testing
#     assert create_app({"TESTING": True}).testing


def test_app_uses_default_config_when_no_option_provided():
    """
    Ensure the app uses the default configuration when no test_config is provided.
    """
    # Act: Create app with no test_config
    app = create_app()

    # Assert: Verify default values from Config
    # TODO: Check if it makes sense to change this test to get values from config.py?
    assert app.config["DEBUG"] is False
    assert app.config["TESTING"] is False
    assert app.config["SECRET_KEY"] == "this-really-needs-to-be-changed"


def test_app_uses_testing_config_when_provided():
    """
    Ensure the app uses the provided test configuration to override defaults.
    """
    # Arrange: Define a testing configuration
    test_config = {
        "TESTING": True,
        "FIRESTORE_COLLECTION": "test_emails",
        "SECRET_KEY": "test-secret",
    }

    # Act: Create app with test_config
    app = create_app(test_config)

    # Assert: Verify the configuration values match the test_config
    assert app.config["TESTING"] is True
    assert app.config["FIRESTORE_COLLECTION"] == "test_emails"
    assert app.config["SECRET_KEY"] == "test-secret"

    # Verify other defaults remain unchanged
    assert app.config["DEBUG"] is False  # Default value not overridden


def test_app_uses_environment_specific_config_configured_in_configpy():
    """
    Ensure the app uses the appropriate configuration class based on FLASK_ENV.
    """
    # Arrange: Set the FLASK_ENV environment variable
    with patch.dict(os.environ, {"FLASK_ENV": "UnitTestingConfig"}):
        # Act: Create the app
        app = create_app()

    # Assert: Verify values specific to UnitTestingConfig
    assert app.config["DEBUG"] is False
    assert app.config["UNIT_TESTING"] is True
    assert app.config["TESTING"] is True


def test_app_defaults_to_production_config_if_flask_env_is_missing():
    """
    Ensure the app defaults to ProductionConfig when FLASK_ENV is not set.
    """
    # Arrange: Ensure FLASK_ENV is not set
    with patch.dict(os.environ, {}, clear=True):
        # Act: Create the app
        app = create_app()

    # Assert: Verify default values from ProductionConfig
    assert app.config["DEBUG"] is False
    assert app.config["TESTING"] is False
    assert app.config["FIRESTORE_COLLECTION"] == "emails"  # Default collection


def test_app_defaults_to_production_config_if_flask_env_is_invalid():
    """
    Ensure the app defaults to ProductionConfig when FLASK_ENV is invalid.
    """
    # Arrange: Set an invalid FLASK_ENV
    with patch.dict(os.environ, {"FLASK_ENV": "InvalidConfig"}):
        # Act: Create the app
        app = create_app()

    # Assert: Verify default values from ProductionConfig
    assert app.config["DEBUG"] is False
    assert app.config["TESTING"] is False
    assert app.config["FIRESTORE_COLLECTION"] == "emails"  # Default collection
