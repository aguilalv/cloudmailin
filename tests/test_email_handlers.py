from cloudmailin.schemas import Email
from cloudmailin.email_handlers import EmailHandler


def test_generic_handler_returns_email_unchanged():
    # Arrange: Create an Email object using the factory method
    email = Email.from_flat_data(
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        date="Mon, 16 Jan 2012 17:00:01 +0000",
    )

    # Act: Process the Email object with the generic handler
    handler = EmailHandler()
    result = handler.handle(email)

    # Assert: The result should match the input Email object
    assert result == email
