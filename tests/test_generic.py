import pytest

from flask import jsonify

# Test 1: Valid payload returns 200 OK
def test_new_generic_email_valid_payload(client):
    email_data = {
            "envelope": {
                "from": "sender@example.com",
                "to": "recipient@example.com"
            },
            "headers": {
                "subject": "Test Email"
            }
        }
    response = client.post(
        "/generic/new",
        json=email_data
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "sender": "sender@example.com",
        "recipient": "recipient@example.com",
        "subject": "Test Email"
    }

# Test 3: Invalid email format in 'from' returns 400
def test_new_generic_email_invalid_from_email(client):
    email_data = {
            "envelope": {
                "from": "sender",
                "to": "recipient@example.com"
            },
            "headers": {
                "subject": "Test Email"
            }
        }
    response = client.post(
        "/generic/new",
        json=email_data
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"][0]["loc"] == ["sender"]

# Test 4: Missing 'subject' in headers returns 400
def test_new_generic_email_missing_subject(client):
    email_data = {
            "envelope": {
                "from": "sender@example.com",
                "to": "recipient@example.com"
            },
            "headers": {
            }
        }
    response = client.post(
        "/generic/new",
        json=email_data
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"][0]["loc"] == ["subject"]
