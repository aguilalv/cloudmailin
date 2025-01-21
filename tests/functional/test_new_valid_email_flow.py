import json
import pytest
import requests
from dotenv import load_dotenv
from google.cloud import firestore

# Load .env file
load_dotenv()

@pytest.fixture(scope="module")
def test_firestore_collection():
    """Fixture to return a Firestore collection for tests."""
    collection_name = "test_emails"
    db = firestore.Client()
    collection = db.collection(collection_name)

    # Clean up the collection before and after the test
    yield collection
    for doc in collection.stream():
        doc.reference.delete()

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
    base_url, valid_real_payload, handler_class, test_firestore_collection
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

    # Verify the email is stored in Firestore
    docs = list(test_firestore_collection.stream())
    assert len(docs) == 1  # Ensure one document is stored

    stored_data = docs[0].to_dict()
    assert stored_data["sender"] == valid_real_payload["envelope"]["from"]
    assert stored_data["recipient"] == valid_real_payload["from"]
    assert stored_data["subject"] == valid_real_payload["haders"]["subject"]
    assert stored_data["plain"] == valid_real_payload["plain"]
    assert stored_data["html"] == valid_real_payload["html"]
