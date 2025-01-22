from unittest.mock import mock_open, patch
from cloudmailin.handler_registry import HandlerRegistry
from cloudmailin import create_app
from textwrap import dedent
import os
import pytest
from cloudmailin.config import ProductionConfig, UnitTestingConfig, Config

@pytest.fixture
def mock_config():
    """
    Mock the config module to provide specific configurations for unit tests.
    """
    mocked_config = {
        "DEBUG": False,
        "TESTING": False,
        "FIRESTORE_COLLECTION": "test_emails",
        "SECRET_KEY": "mock-secret-key",
        "FUNCTIONAL_TESTING": False,
    }

    with patch("cloudmailin.config.Config", mocked_config):
        yield mocked_config

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

def test_app_uses_default_config_when_no_option_provided():
    """
    Ensure the app uses the default configuration when no test_config is provided.
    """
    # Act: Create app with no test_config
    app = create_app()

    # Assert: Verify default values from Config
    for key in vars(Config):
        if not key.startswith("_"):  # Ignore private/internal attributes
            assert app.config[key] == getattr(Config, key), f"{key} does not match Config default"

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
    for key, value in test_config.items():
        assert app.config[key] == value, f"{key} does not match provided value"



    # Verify other defaults remain unchanged
    for key, value in vars(Config).items():
        if not key.startswith("_") and key not in test_config:
            assert app.config[key] == value, f"{key} default not retained"



def test_app_uses_environment_specific_config_configured_in_configpy():
    """
    Ensure the app uses the appropriate configuration class based on FLASK_ENV.
    """
    # Arrange: Dynamically set FLASK_ENV based on the class name
    environment = UnitTestingConfig.__name__
    with patch.dict(os.environ, {"FLASK_ENV": environment}):
        # Act: Create the app
        app = create_app()

    # Assert: Dynamically validate all attributes from UnitTestingConfig
    expected_config_values = {
        key: value for key, value in vars(UnitTestingConfig).items() if not key.startswith("_")
    }
    for key, expected_value in expected_config_values.items():
        assert app.config[key] == expected_value, f"Config field {key} does not match."


def test_app_defaults_to_production_config_if_flask_env_is_missing():
    """
    Ensure the app defaults to ProductionConfig when FLASK_ENV is not set.
    """
    # Arrange: Ensure FLASK_ENV is not set
    with patch.dict(os.environ, {}, clear=True):
        # Act: Create the app
        app = create_app()

    # Assert: Verify all fields match ProductionConfig
    production_config_values = {
        key: value for key, value in vars(ProductionConfig).items() if not key.startswith("_")
    }
    for key, expected_value in production_config_values.items():
        assert app.config[key] == expected_value, f"Config field {key} does not match."



def test_app_defaults_to_production_config_if_flask_env_is_invalid():
    """
    Ensure the app defaults to ProductionConfig when FLASK_ENV is invalid.
    """
    # Arrange: Set an invalid FLASK_ENV
    with patch.dict("os.environ", {"FLASK_ENV": "InvalidConfig"}):
        # Act: Create the app
        app = create_app()

    # Assert: Verify all fields match ProductionConfig
    production_config_values = {
        key: value for key, value in vars(ProductionConfig).items() if not key.startswith("_")
    }
    for key, expected_value in production_config_values.items():
        assert app.config[key] == expected_value, f"Config field {key} does not match."

