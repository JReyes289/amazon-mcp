import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_import_structure():
    """Test that all modules can be imported correctly."""
    # Test importing the main package
    from fewsats_mcp import server
    assert server is not None
    
    # Test importing the Amazon client
    from fewsats_mcp.amazon.client import Amazon
    assert Amazon is not None
    
    # Test that FastMCP instance exists
    assert hasattr(server, 'mcp')
    
def test_amazon_client():
    """Test the Amazon client placeholder functionality."""
    from fewsats_mcp.amazon.client import Amazon
    
    client = Amazon()
    
    # Test search method
    result = client.search("test product", "amazon.com")
    assert "status" in result
    assert result["status"] == "ok"
    
    # Test buy_now method
    shipping = {"address": "test"}
    user = {"name": "test"}
    result = client.buy_now("http://test.url", shipping, user, "ASIN123", 1)
    assert "status_code" in result
    assert result["status_code"] == 402
    
def test_fastapi_instance():
    """Test that FastAPI instance is properly created."""
    from fewsats_mcp import server
    
    # Check that the mcp instance is a FastAPI app
    from fastapi import FastAPI
    assert isinstance(server.mcp, FastAPI)
    
    # Test that handle_response function works
    test_response = {"test": "data"}
    result = server.handle_response(test_response)
    assert result == test_response
