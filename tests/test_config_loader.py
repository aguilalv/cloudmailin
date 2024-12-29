import builtins
import yaml
import pytest
from unittest.mock import patch, mock_open

from cloudmailin import create_app
from cloudmailin.handler_registry import HandlerRegistry, HANDLERS_MAP
from cloudmailin.config_loader import load_config, initialize_handler_registry_from_config


# --- Tests valid configuration file parsed correctly --- #

def test_valid_yaml_config_has_expected_keys(valid_yaml_config):
    """
    Test that a valid YAML configuration parsing produces expected top-level keys and structure.

    Ensures that the configuration defines 'handlers' and each handler has 'steps' and 'senders'.
    """
    with patch("builtins.open", mock_open(read_data=valid_yaml_config)):
        config = load_config("dummy_path.yaml")
        assert "handlers" in config, "Top-level 'handlers' key is missing"
        assert "CampaignClassifierHandler" in config["handlers"], "'CampaignClassifierHandler' key is missing"
        assert "steps" in config["handlers"]["CampaignClassifierHandler"], "'steps' key is missing"
        assert "senders" in config["handlers"]["CampaignClassifierHandler"], "'senders' key is missing"

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


def test_initialize_handler_registry_from_config(valid_yaml_config, app):
    """
    Test that the handler registry is initialized correctly from the YAML configuration.
    """
    with patch("builtins.open", mock_open(read_data=valid_yaml_config)):
        registry = initialize_handler_registry_from_config("dummy_handler_config.yaml")

        assert isinstance(registry, HandlerRegistry)
        assert "newsletter@example.com" in registry._registry
        assert "promo@example.com" in registry._registry
        assert registry.get_handler_for_sender("newsletter@example.com") == HANDLERS_MAP["CampaignClassifierHandler"]
        assert registry.get_handler_for_sender("promo@example.com") == HANDLERS_MAP["CampaignClassifierHandler"]
