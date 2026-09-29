import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_and_get_meeting(client):
    new_meeting = {
        "client": "TestCorp",
        "contact": "Alice Smith, VP Eng",
        "date": "2026-09-25",
        "title": "TestCorp Architecture Discussion",
        "meeting_notes": "Discussed distributed caching and Kubernetes deployment. Budget is $50,000.",
        "decisions": ["Approved Kubernetes architecture"],
        "concerns": ["Need automated failover SLA"],
        "commitments": ["Will provide SLA documentation by Monday"],
        "follow_ups": ["Send SLA doc"]
    }

    create_resp = client.post("/api/meetings", json=new_meeting)
    assert create_resp.status_code == 201
    created_data = create_resp.json()
    assert created_data["client"] == "TestCorp"
    assert created_data["id"] is not None
    assert created_data["hindsight_status"] in ["retained_in_hindsight", "retained_resilient_store"]
    meeting_id = created_data["id"]

    # Get single meeting
    get_resp = client.get(f"/api/meetings/{meeting_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == meeting_id

    # List meetings with client filter
    list_resp = client.get("/api/meetings?client=TestCorp")
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] >= 1


def test_client_insights(client):
    resp = client.get("/api/insights/TestCorp")
    assert resp.status_code == 200
    data = resp.json()
    assert data["client"] == "TestCorp"
    assert data["number_of_interactions"] >= 1
    assert "open_commitments" in data
    assert "recurring_concerns" in data


def test_memory_recall(client):
    recall_req = {
        "client": "TestCorp",
        "query": "Kubernetes and budget requirements"
    }
    resp = client.post("/api/memory/recall", json=recall_req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["client"] == "TestCorp"
    assert "memories" in data
    assert len(data["memories"]) >= 1
