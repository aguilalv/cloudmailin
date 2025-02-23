from typing import List, Callable
from flask import current_app

from cloudmailin.schemas import Email
from cloudmailin.db import get_db

# Define a type alias for step functions
StepFunction = Callable[[Email], Email]


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
        current_app.logger.info(
            f"[{self.__class__.__name__}] Processing email from {email.sender}"
        )

        # Pass the email model through each step
        for step in self.steps:
            email = step(email)

        # Step 3: Store email in database
        #        try:
        db = get_db()
        db.store_email(email.model_dump())
        current_app.logger.info(f"Email stored in database: {email.subject}")
        #        except Exception as e:
        #            current_app.logger.error(
        #                f"Failed to store email in database: {e}", exc_info=True
        #            )

        return email
