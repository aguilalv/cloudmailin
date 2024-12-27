from typing import List, Callable
from flask import current_app

from cloudmailin.schemas import Email


#Define a type alias for step functions
StepFunction = Callable[[Email],Email]

class BaseHandler:
    """
    Base handler for processing emails.
    Provides foundational functionality such as logging.
    """

    steps: List[StepFunction] = []

    def handle(self, email: Email) -> Email:
        """
        Handle an email object: Log a health-related message, apply all steps in sequence and Store in the database.
        """
        # Step 1: Log app health check message
        current_app.logger.info(f"Processing email from {email.sender}")
       
        # Pass the email model through each step
        for step in self.steps:
            email = step(email)

        # Step 3: Store email in database
        #TODO: Replace logger message with code to insert in database
        current_app.logger.info(f"Here I should store in database the email with subject {email.subject}")
        
        return email


