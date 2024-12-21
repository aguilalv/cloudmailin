from cloudmailin.schemas import Email
from cloudmailin.email_handlers import EmailHandler

def test_generic_handler_returns_email_unchanged():
    # Arrange: Create an Email object using the factory method
    email = Email.from_flat_data(
        sender="john@example.com",
        recipient="generic@example.com",
        subject="Test Email"
    )

    # Act: Process the Email object with the generic handler
    handler = EmailHandler()
    result = handler.handle(email)

    # Assert: The result should match the input Email object
    assert result == email
