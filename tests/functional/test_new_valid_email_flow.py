import json
import pytest
import requests


# Assuming valid_email_payload.json exists in the test_data directory
@pytest.fixture
def valid_real_payload():
    """
    Load the valid email payload from the JSON test data file.
    """
    with open("tests/functional/test_data/valid_email_payload.json") as f:
        return json.load(f)


@pytest.mark.parametrize(
    "handler_class",
    [
        "BaseHandler",  # Base handler
        #        "CampaignClassifierHandler",  # Specialized handler
    ],
)
def test_email_processing_flow_with_handler(
    base_url, valid_real_payload, caplog, handler_class
):
    """
    Functional test to verify end-to-end email processing flow:
    - Valid payload is sent to the server.
    - The correct handler processes the email (validated via the response or logs).
    - Email is 'stored' (simulated by checking the response).
    """
    # Arrange
    endpoint = f"{base_url}/generic/new"
    sender = "test_handler@example.com"

    # Update the payload with the unique sender for the handler
    valid_real_payload["envelope"]["from"] = sender

    # Act: Send the payload
    response = requests.post(endpoint, json=valid_real_payload)

    # Assert: Verify the response
    assert (
        response.status_code == 200
    ), f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    # Parse the response JSON for validation
    response_data = response.json()

    # Assert: Verify email processing status
    assert response_data.get("status") == "processed", (
        f"Expected 'processed' status, but got {response_data.get('status')}. "
        f"Response: {response_data}"
    )

    # Assert: Verify the handler used for processing
    assert response_data.get("handler") == "BaseHandler", (
        f"Expected handler 'BaseHandler', but got {response_data.get('handler')}. "
        f"Response: {response_data}"
    )

    # TODO: Add a check that the message has been stored in a database
