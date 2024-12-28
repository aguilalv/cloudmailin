from unittest.mock import Mock

from cloudmailin.handler_registry import HandlerRegistry
from cloudmailin.handlers.base_handler import BaseHandler

# --- Test Initialization and Integration with app context --- #

def test_app_initializes_with_handler_registry(app):
    """
    Test that the app initializes with a handler registry in its config.
    """
    assert 'handler_registry' in app.config
    assert app.config['handler_registry'] is not None
    assert isinstance(app.config['handler_registry'], HandlerRegistry)

# --- Test handler registration and retrieval --- #

def test_handler_registry_register_and_retrieve():
    """
    Test that handlers can be registered and retrieved correctly from the registry.
    """

    registry = HandlerRegistry()
    mock_handler = Mock()
    registry.register("sender@example.com", mock_handler.__class__)

    handler = registry.get_handler_for_sender("sender@example.com")
    assert handler == mock_handler.__class__


def test_handler_registry_defaults_to_generic_handler():
    # Arrange: A sender not mapped to a specific handler
    handler_registry = HandlerRegistry()
    sender = "unknown@example.com"
    
    # Act: Fetch the handler from the registry
    handler_class = handler_registry.get_handler_for_sender(sender)

    # Assert: Ensure it defaults to the GenericHandler
    assert handler_class == BaseHandler

# --- Edge cases --- #

# Test trying to register an invalid handler 
