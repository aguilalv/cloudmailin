import pytest
from cloudmailin.schemas import Email
from cloudmailin.handlers.steps import assign_campaign_type

# --- Test step-specific logic: assign_campaign_type --- #

def test_assign_campaign_type_with_matching_subject(valid_flat_payload):
    """
    Test that assign_campaign_type assigns the correct campaign type
    based on a matching subject keyword.
    """
    valid_flat_payload["subject"] = "Spring Sale Campaign"
    email = Email.from_flat_data(**valid_flat_payload)

    result = assign_campaign_type(email)

    assert result.campaign_type == "promotion"


def test_assign_campaign_type_with_no_match(valid_flat_payload):
    """
    Test that assign_campaign_type assigns a default campaign type
    when no conditions are met.
    """
    valid_flat_payload["subject"] = "Unrelated Subject"
    email = Email.from_flat_data(**valid_flat_payload)

    result = assign_campaign_type(email)

    assert result.campaign_type == "unclassified"

# --- Test Field Integrity --- #

def test_assign_campaign_type_does_not_modify_unrelated_fields(valid_flat_payload):
    """
    Test that assign_campaign_type does not modify unrelated fields.
    """
#    valid_flat_payload["subject"] = "Unrelated Subject"
    email = Email.from_flat_data(**valid_flat_payload)

    # Create a copy of the original email
    original_email = email.model_copy()

    # Apply the step
    result = assign_campaign_type(email)

    # Check that all fields, except campaign_type, remain unchanged
    for field in email.model_fields_set:
        if field != "campaign_type":
            assert getattr(result, field) == getattr(original_email, field), f"Field '{field}' was unexpectedly modified"

# --- Test edge cases --- #

# Test empty subject or subject with special characters (Parametric)
