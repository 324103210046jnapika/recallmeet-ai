from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from .memory import MemoryItem, MemoryOperationInfo


class MeetingPrepareRequest(BaseModel):
    client: str = Field(..., description="Client or company name", examples=["Acme Corporation"])
    upcoming_context: str = Field(..., description="Context for upcoming meeting (title, goal, participants)", examples=["Sprint planning & security sign-off meeting with Sarah Chen (CTO)"])
    user_question: Optional[str] = Field(None, description="Optional specific focus or question for the AI agent", examples=["What were our exact promises regarding RBAC and security documentation?"])
    memory_enabled: bool = Field(default=True, description="Toggle Hindsight memory ON/OFF for hackathon demonstration")


class MeetingPrepareResponse(BaseModel):
    client: str
    upcoming_context: str
    memory_enabled: bool
    hindsight_connected: bool
    memory_provider: Literal["hindsight", "local_fallback", "none"] = Field(..., description="Explicit memory provider used: 'hindsight', 'local_fallback', or 'none'")
    memory_info: MemoryOperationInfo = Field(..., description="Detailed memory operation telemetry")
    executive_summary: str
    client_priorities: List[str] = Field(default_factory=list)
    previous_commitments: List[str] = Field(default_factory=list)
    open_action_items: List[str] = Field(default_factory=list)
    unresolved_concerns: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    suggested_agenda: List[str] = Field(default_factory=list)
    talking_points: List[str] = Field(default_factory=list)
    questions_to_ask: List[str] = Field(default_factory=list)
    recommended_next_steps: List[str] = Field(default_factory=list)
    memory_sources: List[MemoryItem] = Field(default_factory=list)
    reflection_summary: Optional[str] = Field(None, description="High-level synthesis from Hindsight reflect operation if available")
