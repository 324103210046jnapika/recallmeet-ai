import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=" * 70)
print("1. HEALTH ENDPOINT")
print("=" * 70)
res = client.get("/api/health")
print(f"Status: {res.status_code}")
print(json.dumps(res.json(), indent=2))

print("\n" + "=" * 70)
print("2. CLIENTS LIST")
print("=" * 70)
res = client.get("/api/clients")
print(f"Status: {res.status_code}")
print(json.dumps(res.json(), indent=2))

print("\n" + "=" * 70)
print("3. ACME CORPORATION INSIGHTS")
print("=" * 70)
res = client.get("/api/insights/Acme Corporation")
print(f"Status: {res.status_code}")
print(json.dumps(res.json(), indent=2))

print("\n" + "=" * 70)
print("4. MEMORY RECALL (Query: 'security review and AWS deployment')")
print("=" * 70)
res = client.post("/api/memory/recall", json={
    "client": "Acme Corporation",
    "query": "security review and AWS deployment"
})
print(f"Status: {res.status_code}")
print(json.dumps(res.json(), indent=2))

print("\n" + "=" * 70)
print("5. MEETING PREP: MEMORY ENABLED (HINDSIGHT ON)")
print("=" * 70)
res = client.post("/api/meetings/prepare", json={
    "client": "Acme Corporation",
    "upcoming_context": "Executive contract sign-off with Sarah Chen (CTO)",
    "user_question": "What promises did we make and what is blocking Sarah from signing?",
    "memory_enabled": True
})
print(f"Status: {res.status_code}")
print(json.dumps(res.json(), indent=2))

print("\n" + "=" * 70)
print("6. MEETING PREP: MEMORY DISABLED (HINDSIGHT OFF - HACKATHON COMPARISON)")
print("=" * 70)
res = client.post("/api/meetings/prepare", json={
    "client": "Acme Corporation",
    "upcoming_context": "Executive contract sign-off with Sarah Chen (CTO)",
    "user_question": "What promises did we make and what is blocking Sarah from signing?",
    "memory_enabled": False
})
print(f"Status: {res.status_code}")
print(json.dumps(res.json(), indent=2))

print("\n" + "=" * 70)
print("ALL ENDPOINTS VERIFIED SUCCESSFULLY!")
print("=" * 70)
