
import pytest
from unittest.mock import patch, call
from cloudmailin.handlers.base_handler import BaseHandler
from cloudmailin.schemas import Email

# --- Test logging behaviour --- #

def test_base_handler_logs_health_message(valid_flat_payload, app):
    """
    Test that BaseHandler logs a health-related message when handling an email.
    """
    email = Email.from_flat_data(**valid_flat_payload)
    handler = BaseHandler()

    with patch.object(app.logger, "info") as mock_logger:
        handler.handle(email)
        mock_logger.assert_any_call("Processing email from sender@example.com")

# --- Test basic operations and step execution --- #

def test_base_handler_executes_steps_in_order(valid_flat_payload, app):
    """
    Test that BaseHandler executes steps in the correct order,
    passing the modified email object through each step.
    """
    # Arrange 
    def step_one(email):
        email.subject += " Step1"
        return email
    
    def step_two(email):
        email.subject += " Step2"
        return email
    
    class TestHandler(BaseHandler):
        steps = [step_one, step_two]
   
    email = Email.from_flat_data(**valid_flat_payload)
    handler = TestHandler()

    # Act
    with app.app_context():
        result = handler.handle(email)
    
    # Assert
    assert result.subject == "Test Subject Step1 Step2"


def test_base_handler_stores_final_email_model(app, valid_flat_payload):
    """
    Test that the final modified email model is passed to the storage step to be stored in the database.
    """
    email = Email.from_flat_data(**valid_flat_payload)

    # Define two sample steps to modify the email
    def step_one(email):
        email.subject += " Step1"
        return email
    
    def step_two(email):
        email.subject += " Step2"
        return email
    
    class TestHandler(BaseHandler):
        steps = [step_one, step_two]

    handler = TestHandler()
    
    with patch.object(app.logger, "info") as mock_logger:
        result = handler.handle(email)
    
    # Assert that the storage log was called with the final modified email
    expected_final_subject = "Test Subject Step1 Step2"
    
    # Verify the final email subject is as expected (Sanity check)
    assert result.subject == expected_final_subject
    
    # Verify the logger received the final email's subject indirectly
    storage_call = [call for call in mock_logger.call_args_list if "store in database" in call.args[0]]
    assert storage_call, "Expected a storage log call but none was found."
    assert expected_final_subject in storage_call[0].args[0], "Storage log did not include the final email subject."

# --- Edge cases --- #

