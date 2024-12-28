from cloudmailin.handlers.base_handler import BaseHandler

DEFAULT_HANDLER = BaseHandler


class HandlerRegistry:
    """Registry for mapping email senders to handlers."""

    def __init__(self):
        self._registry = {}

    def register(self, sender: str, handler_class):
        """
        Register a handler for a specific sender.

        Args:
            sender (str): The email sender address.
            handler_class (type): The handler class to register.

        Raises:
            ValueError: If handler_class is not a valid class or lacks a handle method.
        """
        if not isinstance(handler_class, type):
            raise ValueError("Handler must be a class")
        
        if not hasattr(handler_class, 'handle') or not callable(getattr(handler_class, 'handle')):
            raise ValueError("Handler class must have a callable 'handle' method")

        self._registry[sender] = handler_class

    def get_handler_for_sender(self, sender: str):
        """
        Fetch the handler for a sender, falling back to the default handler.

        Args:
            sender (str): The email sender address.

        Returns:
            type: The handler class for the sender.
        """
        return self._registry.get(sender, DEFAULT_HANDLER)

