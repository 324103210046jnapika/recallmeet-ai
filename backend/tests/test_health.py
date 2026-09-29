import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure backend root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "RecallMeet AI"
    assert "hindsight" in data
    assert "hindsight_configured" in data
    assert "hindsight_reachable" in data
    assert "hindsight_bank" in data
    assert "last_operation_status" in data
    assert "llm" in data
    assert "stats" in data

