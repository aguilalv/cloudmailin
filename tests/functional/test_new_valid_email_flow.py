import json
import pytest
import requests
from dotenv import load_dotenv
from google.cloud import firestore
import os

from cloudmailin.config import FunctionalTestingConfig

# Load .env file
load_dotenv()

# Assuming valid_email_payload.json exists in the test_data directory
@pytest.fixture
def valid_real_payload():
    """
    Load the valid email payload from the JSON test data file.
    """
    with open("tests/functional/test_data/valid_email_payload.json") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def functional_firestore_collection():
    """Fixture to clean up the Firestore collection before and after the test."""
    collection_name = FunctionalTestingConfig.FIRESTORE_COLLECTION
    db = firestore.Client()
    collection = db.collection(collection_name)

    # Clean up before the test
#    for doc in collection.stream():
#       doc.reference.delete()

    yield collection

    # Clean up after the test


#    for doc in collection.stream():
#        doc.reference.delete()


@pytest.fixture(scope="session", autouse=True)
def validate_functional_env():
    flask_env = os.getenv("FLASK_ENV")
    if flask_env != "FunctionalTestingConfig":
        raise RuntimeError(
            f"Functional tests require FLASK_ENV=FunctionalTestingConfig, but got {flask_env or 'None'}."
        )


@pytest.mark.parametrize(
    "handler_class",
    [
        "BaseHandler",  # Base handler
        #        "CampaignClassifierHandler",  # Specialized handler
    ],
)
@pytest.mark.functional
def test_email_processing_flow_with_handler(
    base_url, valid_real_payload, handler_class
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
    valid_real_payload["envelope"]["from"] = sender

    # Setup Firestore client and collection
    db = firestore.Client()
    collection_name = os.getenv("FIRESTORE_COLLECTION", "functional_test_emails")
    collection = db.collection(collection_name)

    # Cleanup before the test
    for doc in collection.stream():
        doc.reference.delete()

    # Act: Send the payload
    response = requests.post(endpoint, json=valid_real_payload)

    # Assert: Verify the response
    assert (
        response.status_code == 200
    ), f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    response_data = response.json()
    assert response_data.get("status") == "processed"
    assert response_data.get("handler") == handler_class

    # Verify the email is stored in Firestore
    docs = list(collection.stream())
 
    assert len(docs) == 1  # Ensure one document is stored

    stored_data = docs[0].to_dict()
    assert stored_data["sender"] == valid_real_payload["envelope"]["from"]
    assert stored_data["recipient"] == valid_real_payload["envelope"]["to"]
    assert stored_data["subject"] == valid_real_payload["headers"]["subject"]
    assert stored_data["plain"] == valid_real_payload["plain"]
    assert stored_data["html"] == valid_real_payload["html"]

    # Cleanup after the test
    # for doc in collection.stream():
    #     doc.reference.delete()
