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
        # Step 1: Log app health check message
        current_app.logger.info(f"Processing email from {email.sender}")
        
        # Step 3: Store email in database
        #TODO: Replace logger message with code to insert in database
        current_app.logger.info(f"Here I should store in database [Dummy message to replace with real code]")
        
        return email


