def test_health_check_endpoint(client):
    """
    Test the health check endpoint returns the correct response.
    """
    response = client.get("/health/")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "deployed_at" in data
