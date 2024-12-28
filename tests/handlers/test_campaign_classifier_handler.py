
import pytest

from cloudmailin.schemas import Email
from cloudmailin.handlers.campaign_classifier import CampaignClassifierHandler
from cloudmailin.handlers.steps import assign_campaign_type

# --- Test handler-specific: Test handle is made of the right steps --- #

def test_campaign_classifier_handler_has_correct_steps():
    """
    Test that CampaignClassifierHandler includes only the assign_campaign_type step.
    """
    handler = CampaignClassifierHandler()
    assert handler.steps == [assign_campaign_type], "Handler should include only the assign_campaign_type step"

# --- Test edge cases --- #

# Test malformed or incomplete email data --- #

# --- Test Handler integration --- #

@pytest.mark.parametrize(
    "field, value, expected_campaign_type",
    [
        ("subject", "Special Sale", "promotion"),
        ("subject", "Meeting Invitation", "unclassified"),
        ("subject", "Weekly Newsletter", "unclassified"),
        ("subject", "Random Subject", "unclassified"),
    ],
)
def test_campaign_classifier_handler_integration(app, valid_flat_payload, field, value, expected_campaign_type):
    """
    Integration test to verify that CampaignClassifierHandler processes an Email object correctly,
    assigning campaign_type based on a dynamic field while leaving other fields untouched.
    """
    # Arrange
    email = Email.from_flat_data(**valid_flat_payload)
    setattr(email, field, value)  # Dynamically set the field
    original_email = email.model_copy()  # Create a copy for comparison

    handler = CampaignClassifierHandler()

    # Act
    with app.app_context():
        result = handler.handle(email)

    # Assert: Check the campaign_type was correctly set
    assert result.campaign_type == expected_campaign_type, f"Expected campaign_type '{expected_campaign_type}' for {field}='{value}'"

    # Assert: Verify no other fields were changed
    for model_field in email.model_fields_set:
        if model_field != "campaign_type":
            assert getattr(result, model_field) == getattr(original_email, model_field), f"Field '{model_field}' was unexpectedly modified"



