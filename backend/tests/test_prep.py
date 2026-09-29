import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_prepare_meeting_with_memory_on(client):
    # First ensure a meeting exists for the client
    client.post("/api/meetings", json={
        "client": "Acme Prep Test",
        "contact": "Sarah Chen, CTO",
        "date": "2026-09-20",
        "title": "Security Deep Dive",
        "meeting_notes": "Sarah requires AWS deployment and strict RBAC. Security review remains unresolved.",
        "decisions": ["AWS deployment target"],
        "concerns": ["Security review pending InfoSec validation"],
        "commitments": ["Engineering team committed to deliver final security plan"],
        "follow_ups": ["Schedule InfoSec sync"]
    })

    prep_req = {
        "client": "Acme Prep Test",
        "upcoming_context": "Executive sign-off and timeline meeting with CTO Sarah Chen",
        "user_question": "What are the unresolved security blockers?",
        "memory_enabled": True
    }

    resp = client.post("/api/meetings/prepare", json=prep_req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["memory_enabled"] is True
    assert "memory_provider" in data
    assert data["memory_provider"] in ["hindsight", "local_fallback"]
    assert "memory_info" in data
    assert data["memory_info"]["provider"] == data["memory_provider"]
    assert "executive_summary" in data
    assert len(data["client_priorities"]) > 0
    assert len(data["unresolved_concerns"]) > 0
    assert len(data["talking_points"]) > 0
    assert len(data["questions_to_ask"]) > 0
    assert len(data["recommended_next_steps"]) > 0



def test_prepare_meeting_with_memory_off(client):
    prep_req = {
        "client": "Acme Prep Test",
        "upcoming_context": "Executive sign-off and timeline meeting with CTO Sarah Chen",
        "memory_enabled": False
    }

    resp = client.post("/api/meetings/prepare", json=prep_req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["memory_enabled"] is False
    assert "executive_summary" in data
    assert "MEMORY DISABLED" in data["executive_summary"] or "Unknown" in data["client_priorities"][0]
    # Memory sources must be empty when memory is disabled
    assert len(data["memory_sources"]) == 0
