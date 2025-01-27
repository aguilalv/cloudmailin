import pytest
from unittest.mock import patch, mock_open

import yaml

from cloudmailin.handlers.base_handler import BaseHandler

from cloudmailin.handler_registry import (
    HandlerRegistry,
    HANDLERS_MAP,
    load_config,
    initialize_handler_registry_from_config,
)

# --- Test Initialization and Integration with app context --- #


def test_app_initializes_with_handler_registry(app_factory):
    """
    Test that the app initializes with a handler registry in its config.
    """
    app = app_factory()
    assert "handler_registry" in app.config
    assert app.config["handler_registry"] is not None
    assert isinstance(app.config["handler_registry"], HandlerRegistry)


# --- Test handler registration and retrieval --- #


def test_handler_registry_register_and_retrieve():
    """
    Test that handlers can be registered and retrieved correctly from the registry.
    """

    # Define a Mock handler class with a handle method to comply with the expected contract
    class MockHandler:
        def handle(self, email):
            return email

    registry = HandlerRegistry()
    mock_handler = MockHandler()
    registry.register("sender@example.com", mock_handler.__class__)

    handler = registry.get_handler_for_sender("sender@example.com")
    assert handler == MockHandler


def test_handler_registry_defaults_to_generic_handler():
    # Arrange: A sender not mapped to a specific handler
    handler_registry = HandlerRegistry()
    sender = "unknown@example.com"

    # Act: Fetch the handler from the registry
    handler_class = handler_registry.get_handler_for_sender(sender)

    # Assert: Ensure it defaults to the GenericHandler
    assert handler_class == BaseHandler


# --- Edge cases --- #


@pytest.mark.parametrize("invalid_handler", [None, 123, "not_a_class", [], {}])
def test_handler_registry_rejects_invalid_handler(invalid_handler):
    """
    Test that the handler registry rejects invalid handler classes.
    """
    registry = HandlerRegistry()

    with pytest.raises(ValueError, match="Handler must be a class"):
        registry.register("sender@example.com", invalid_handler)


# --- Tests valid configuration file parsed correctly --- #


def test_valid_yaml_config_has_expected_keys(valid_yaml_config):
    """
    Test that a valid YAML configuration parsing produces expected top-level keys and structure.

    Ensures that the configuration defines 'handlers' and each handler has 'steps' and 'senders'.
    """
    with patch("builtins.open", mock_open(read_data=valid_yaml_config)):
        config = load_config("dummy_path.yaml")
        assert "handlers" in config, "Top-level 'handlers' key is missing"
        assert (
            "CampaignClassifierHandler" in config["handlers"]
        ), "'CampaignClassifierHandler' key is missing"
        assert (
            "steps" in config["handlers"]["CampaignClassifierHandler"]
        ), "'steps' key is missing"
        assert (
            "senders" in config["handlers"]["CampaignClassifierHandler"]
        ), "'senders' key is missing"


def test_valid_yaml_config_parses_steps(valid_yaml_config):
    """
    Test that the steps in a valid YAML configuration are correctly parsed.
    """
    with patch("builtins.open", mock_open(read_data=valid_yaml_config)):
        config = load_config("dummy_path.yaml")
        steps = config["handlers"]["CampaignClassifierHandler"]["steps"]
        assert steps == ["cloudmailin.handlers.steps.assign_campaign_type"]


def test_valid_yaml_config_parses_senders(valid_yaml_config):
    """
    Test that the senders in a valid YAML configuration are correctly parsed.
    """
    with patch("builtins.open", mock_open(read_data=valid_yaml_config)):
        config = load_config("dummy_path.yaml")
        senders = config["handlers"]["CampaignClassifierHandler"]["senders"]
        assert senders == ["newsletter@example.com", "promo@example.com"]


# --- Test Invalid Configurations --- #


@pytest.mark.parametrize(
    "invalid_part, modification",
    [
        ("root", {"invalid_root": "something"}),  # Replace root entirely
        ("handlers.CampaignClassifierHandler.steps", None),  # Remove steps
        ("handlers.CampaignClassifierHandler.senders", None),  # Remove senders
    ],
)
def test_load_invalid_yaml_configs(valid_yaml_config, invalid_part, modification):
    """
    Parametrized test for various invalid YAML configurations.

    Each test modifies a specific part of the valid configuration and expects a ValueError.
    """
    # Parse the valid YAML into a Python dict
    config = yaml.safe_load(valid_yaml_config)

    # Handle root-level modification explicitly
    if invalid_part == "root":
        config = modification  # Directly replace the root with invalid content
    else:
        # Apply nested modification dynamically
        keys = invalid_part.split(".")
        target = config
        for key in keys[:-1]:
            target = target.setdefault(key, {})
        target[keys[-1]] = modification

    # Dump the modified config back to YAML format
    invalid_yaml = yaml.dump(config)

    # Test if invalid configuration raises an exception
    with patch("builtins.open", mock_open(read_data=invalid_yaml)):
        with pytest.raises(ValueError):
            load_config("dummy_path.yaml")


# --- Test config initialization --- #


def test_initialize_handler_registry_from_config(valid_yaml_config, app_factory):
    """
    Test that the handler registry is initialized correctly from the YAML configuration.
    """
    # app = app_factory()

    with patch("builtins.open", mock_open(read_data=valid_yaml_config)):
        registry = initialize_handler_registry_from_config("dummy_handler_config.yaml")

        assert isinstance(registry, HandlerRegistry)
        assert "newsletter@example.com" in registry._registry
        assert "promo@example.com" in registry._registry
        assert (
            registry.get_handler_for_sender("newsletter@example.com")
            == HANDLERS_MAP["CampaignClassifierHandler"]
        )
        assert (
            registry.get_handler_for_sender("promo@example.com")
            == HANDLERS_MAP["CampaignClassifierHandler"]
        )
