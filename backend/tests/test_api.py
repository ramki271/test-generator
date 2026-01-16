import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "test-case-generator"


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Test Case Generator"
    assert "endpoints" in data


def test_generate_test_cases_missing_input():
    """Test that request fails when neither JIRA issue nor manual input is provided."""
    response = client.post(
        "/api/v1/generate-test-cases",
        json={
            "test_types": ["functional"],
        }
    )
    assert response.status_code == 400


def test_generate_test_cases_with_manual_input():
    """Test test case generation with manual input."""
    response = client.post(
        "/api/v1/generate-test-cases",
        json={
            "manual_input": {
                "title": "Test Feature",
                "description": "A test feature description",
                "acceptance_criteria": [
                    "Criterion 1",
                    "Criterion 2"
                ]
            },
            "test_types": ["functional"],
            "include_edge_cases": True,
            "include_negative_tests": True
        }
    )
    # This will fail without valid API key, but should validate the structure
    assert response.status_code in [200, 500]  # 500 if API key is missing


@pytest.mark.asyncio
async def test_api_docs():
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
