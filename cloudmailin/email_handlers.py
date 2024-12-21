from cloudmailin.schemas import Email


class EmailHandler:
    def handle(self, email: Email) -> Email:
        """Process a validated Email object and return it unchanged."""
        return email
