from cloudmailin.schemas import Email
from cloudmailin.email_handlers import EmailHandler


def test_generic_handler_returns_email_unchanged():
    # Arrange: Create an Email object using the factory method
    email = Email.from_flat_data(
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        date="Mon, 16 Jan 2012 17:00:01 +0000",
        plain="Test Plain Body.",
        html='<html><head>\n<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body\n bgcolor="#FFFFFF" text="#000000">\nTest with <span style="font-weight: bold;">HTML</span>.<br>\n</body>\n</html>',
    )

    # Act: Process the Email object with the generic handler
    handler = EmailHandler()
    result = handler.handle(email)

    # Assert: The result should match the input Email object
    assert result == email
