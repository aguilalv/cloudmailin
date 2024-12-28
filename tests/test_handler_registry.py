from cloudmailin.handler_registry import handler_registry
from cloudmailin.handlers.base_handler import BaseHandler


def test_handler_registry_defaults_to_generic_handler():
    # Arrange: A sender not mapped to a specific handler
    sender = "unknown@example.com"

    # Act: Fetch the handler from the registry
    handler_class = handler_registry.get_handler_for_sender(sender)

    # Assert: Ensure it defaults to the GenericHandler
    assert handler_class == BaseHandler
