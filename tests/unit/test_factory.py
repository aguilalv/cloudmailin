from unittest.mock import patch

from cloudmailin.handler_registry import HandlerRegistry
from cloudmailin import create_app

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


def test_create_app_testing_flag_only_on_when_initialized():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
