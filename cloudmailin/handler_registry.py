from cloudmailin.handlers.base_handler import BaseHandler

DEFAULT_HANDLER = BaseHandler


class HandlerRegistry:
    """Registry for mapping email senders to handlers."""

    def __init__(self):
        self._registry = {}

    def register(self, sender: str, handler_class):
        """Register a handler for a specific sender."""
        self._registry[sender] = handler_class

    def get_handler_for_sender(self, sender: str):
        """Fetch the handler for a sender, falling back to the default handler."""
        return self._registry.get(sender, DEFAULT_HANDLER)

