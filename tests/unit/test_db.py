from flask import g, Flask
from unittest.mock import patch, MagicMock
import logging
import pytest

from cloudmailin import create_app, db
from cloudmailin.db import DatabaseHelper


def test_first_call_to_test_db_creates_and_stores_database_helper_in_g(app_factory):
    """
    Test that the first call to get_db creates and stores the DatabaseHelper instance in Flask's g.
    """
    # Arrange
    app = app_factory()

    with app.app_context():
        # Mock DatabaseHelper
        with patch("cloudmailin.db.DatabaseHelper") as MockDatabaseHelper:
            mock_instance = MockDatabaseHelper.return_value

            # Act
            helper_instance = db.get_db()

            # Assert that the instance stored in g.db is the database helper created by get_db
            assert g.db == helper_instance
            # Assert that get_db returned the instance that we mocked
            assert g.db == mock_instance


def test_subsequent_calls_to_get_db_return_same_helper_instance(app_factory):
    """
    Ensure get_db returns the same DatabaseHelper instance for subsequent calls.
    """
    # Arrange
    app = app_factory()

    with app.app_context():
        # Mock DatabaseHelper
        with patch("cloudmailin.db.DatabaseHelper") as MockDatabaseHelper:
            mock_instance = MockDatabaseHelper.return_value

            # Act: Call get_db twice
            first_call = db.get_db()
            second_call = db.get_db()

            # Assert: Both calls return the same instance
            assert first_call == second_call
            assert first_call == mock_instance

            # Assert: DatabaseHelper is only initialized once
            MockDatabaseHelper.assert_called_once()


# --- Tests for the database helper --- #


@patch("cloudmailin.db.firestore.Client")
def test_store_email_uses_firestore_collection_from_config(mock_firestore_client, app_factory):
    """
    Ensure store_email adds data to the correct Firestore collection based on the environment.
    """
    app = app_factory({"FIRESTORE_COLLECTION": "unit_test_emails"})

    with app.app_context():

        # Arrange
        helper = DatabaseHelper(app.config)
        mock_collection = MagicMock()
        mock_firestore_client.return_value.collection.return_value = mock_collection
        email_data = {"sender": "test@example.com"}

        # Act
        helper.store_email(email_data)

        # Assert: Verify the correct collection is used
        mock_firestore_client.return_value.collection.assert_called_once_with(
            "unit_test_emails"
        )


@patch("cloudmailin.db.firestore.Client")
def test_store_email_adds_document(mock_firestore_client, app_factory):
    """
    Ensure store_email adds the email document to the Firestore collection.
    """
    app = app_factory({"FIRESTORE_COLLECTION": "custom_collection"})

    with app.app_context():
        # Arrange
        helper = DatabaseHelper(app.config)
        mock_collection = MagicMock()
        mock_firestore_client.return_value.collection.return_value = mock_collection
        email_data = {"sender": "test@example.com", "subject": "Hello World"}

        # Act
        helper.store_email(email_data)

        # Assert: Verify the document is added to the collection
        mock_collection.add.assert_called_once_with(email_data)


@patch("cloudmailin.db.firestore.Client")
def test_store_email_logs_error_on_failure(mock_firestore_client, app_factory, caplog):
    """
    Ensure store_email logs an error if Firestore raises an exception.
    """
    app = app_factory({"FIRESTORE_COLLECTION": "custom_collection"})

    with app.app_context():
        # Arrange
        helper = DatabaseHelper(app.config)
        mock_collection = MagicMock()
        mock_collection.add.side_effect = Exception("Firestore error")
        mock_firestore_client.return_value.collection.return_value = mock_collection

        email_data = {"sender": "test@example.com", "subject": "Hello World"}

        # Act
        helper.store_email(email_data)

        print("Captured records:", [record.message for record in caplog.records])

        # Assert: Ensure the error was logged
        assert "Failed to store email in database: Firestore error" in caplog.text


def test_missing_firestore_collection_raises_error(app_factory):
    """
    Test that DatabaseHelper raises a ValueError if FIRESTORE_COLLECTION is missing.
    """
    # Arrange: Create an app without FIRESTORE_COLLECTION in the config
    #app = app_factory(custom_config={"TESTING": True})
    app = app_factory(custom_config={"TESTING": True, "FIRESTORE_COLLECTION": None})

    # Act & Assert: Attempting to initialize DatabaseHelper should raise ValueError
    with app.app_context():
        with pytest.raises(ValueError, match="FIRESTORE_COLLECTION is required but not configured."):
            DatabaseHelper(app.config)

