import yaml

from cloudmailin.handler_registry import HANDLERS_MAP, HandlerRegistry


def load_config(path: str) -> dict:
    """
    Load and parse a YAML configuration file, with structure validation.

    Args:
        path (str): Path to the YAML configuration file.

    Returns:
        dict: Parsed and validated configuration data.

    Raises:
        ValueError: If the configuration structure is invalid.
    """
    with open(path, "r") as file:
        config = yaml.safe_load(file)

    # Validate top-level structure
    if not isinstance(config, dict) or "handlers" not in config:
        raise ValueError("Invalid configuration: Missing 'handlers' section.")

    # Validate each handler
    for handler, details in config["handlers"].items():
        if not isinstance(details, dict):
            raise ValueError(f"Invalid configuration: Handler '{handler}' must map to a dictionary.")

        if "steps" not in details or not isinstance(details["steps"], list):
            raise ValueError(f"Invalid configuration: Handler '{handler}' must have a 'steps' list.")

        if "senders" not in details or not isinstance(details["senders"], list):
            raise ValueError(f"Invalid configuration: Handler '{handler}' must have a 'senders' list.")

    return config

def initialize_handler_registry_from_config(config_file: str) -> HandlerRegistry:
    """
    Load handler configuration from a YAML file and initialize the handler registry.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        HandlerRegistry: An initialized handler registry.
    """
    config = load_config(config_file)

    registry = HandlerRegistry()

    for handler_name, details in config.get("handlers", {}).items():
        if handler_name not in HANDLERS_MAP:
            raise ValueError(f"Handler '{handler_name}' is not defined in HANDLERS_MAP")

        handler_class = HANDLERS_MAP[handler_name]
        for sender in details.get("senders", []):
            registry.register(sender, handler_class)

    return registry

