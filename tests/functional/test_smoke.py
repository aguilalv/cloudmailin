import requests

def test_healthcheck(base_url):
    """
    Test the health check endpoint for a 200 response and the expected data structure.
    """
    healthcheck_url = f"{base_url}/health"
    response = requests.get(healthcheck_url)
    json_data = response.json()
    
    # Verify the response status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    # Verify the "status" field is "healthy"
    assert json_data["status"] == "healthy", f"Unexpected status: {json_data['status']}"
    
    # Verify the response payload structure
    expected_keys = {"status", "version", "deployed_at"}
    assert expected_keys.issubset(json_data.keys()), f"Missing keys in response: {expected_keys - json_data.keys()}"

    # Optional: Log the version and deployment timestamp for debugging purposes
    print(f"Version: {json_data['version']}, Deployed At: {json_data['deployed_at']}")
