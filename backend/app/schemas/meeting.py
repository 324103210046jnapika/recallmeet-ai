from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from .memory import MemoryOperationInfo


class MeetingCreate(BaseModel):
    client: str = Field(..., description="Client or company name (e.g., Acme Corporation)", examples=["Acme Corporation"])
    contact: str = Field(..., description="Primary contact name and title", examples=["Sarah Chen, CTO"])
    date: str = Field(..., description="Date of meeting in YYYY-MM-DD or readable format", examples=["2026-09-20"])
    title: str = Field(..., description="Meeting title or subject", examples=["Architecture & Cloud Strategy"])
    meeting_notes: str = Field(..., description="Detailed notes, discussion topics, and context", examples=["Sarah confirmed preference for AWS deployment. Stressed that RBAC is mandatory."])
    decisions: Optional[List[str]] = Field(default_factory=list, description="Key decisions made during meeting")
    concerns: Optional[List[str]] = Field(default_factory=list, description="Client objections, risks, or open concerns raised")
    commitments: Optional[List[str]] = Field(default_factory=list, description="Promises, deliverables, or commitments made to the client")
    follow_ups: Optional[List[str]] = Field(default_factory=list, description="Action items, deliverables, and next meeting tasks")


class MeetingResponse(MeetingCreate):
    id: str = Field(..., description="Unique meeting identifier")
    retained_memory_id: Optional[str] = Field(None, description="Hindsight retained memory reference ID")
    hindsight_status: str = Field(..., description="Status of memory ingestion ('retained_in_hindsight' or 'retained_resilient_store')")
    memory_provider: Literal["hindsight", "local_fallback"] = Field(..., description="Explicit memory provider used: 'hindsight' or 'local_fallback'")
    memory_info: Optional[MemoryOperationInfo] = Field(None, description="Detailed memory retention telemetry")
    created_at: str = Field(..., description="ISO creation timestamp")


class MeetingListResponse(BaseModel):
    total: int
    client: Optional[str] = None
    meetings: List[MeetingResponse]
