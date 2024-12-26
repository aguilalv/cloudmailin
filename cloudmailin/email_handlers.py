from cloudmailin.schemas import Email
from flask import current_app
from cloudmailin.schemas import Email


class BaseHandler:
    """
    Base handler for processing emails.
    Provides foundational functionality such as logging.
    """

    def handle(self, email: Email):
        """
        Handle an email object and log a health-related message.
        """
        current_app.logger.info(f"Processing email from {email.sender}")
        return email

### OLD - TO DELETE ###

class EmailHandler:
    def handle(self, email: Email) -> Email:
        """Process a validated Email object and return it unchanged."""
        return email


