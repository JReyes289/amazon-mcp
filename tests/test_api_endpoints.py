import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fewsats_mcp.server import mcp

client = TestClient(mcp)

def test_api_docs():
    """Test that the API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_openapi_spec():
    """Test that the OpenAPI specification is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
    # Check that the API spec contains our endpoints
    spec = response.json()
    assert "paths" in spec
    assert "/amazon/search" in spec["paths"]
    assert "/amazon/payment-offers" in spec["paths"]

def test_amazon_search_endpoint():
    """Test the Amazon search endpoint."""
    # Since we're using query parameters for POST, we'll test with JSON body
    test_data = {
        "q": "test product",
        "domain": "amazon.com"
    }
    
    # Note: Our current implementation expects query parameters, not JSON body
    # This test will help us identify this design issue
    response = client.post("/amazon/search", params=test_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "status" in result or isinstance(result, list)

def test_health_check():
    """Test that the server is responding."""
    # Test root endpoint (should return 404 since it's not defined, but server is running)
    response = client.get("/")
    # FastAPI returns 404 for undefined routes, which means the server is working
    assert response.status_code == 404
