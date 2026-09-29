from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class MemoryOperationInfo(BaseModel):
    provider: Literal["hindsight", "local_fallback", "none"] = Field(..., description="Active memory provider")
    operations: List[str] = Field(default_factory=list, description="Operations executed (retain, recall, reflect)")
    bank_id: str = Field(..., description="Memory bank identifier")
    memory_count: int = Field(0, description="Total memories retained or recalled")
    connected: bool = Field(False, description="Whether live Hindsight API was reached")
    message: Optional[str] = Field(None, description="Diagnostic notice")


class MemoryRecallRequest(BaseModel):
    client: str = Field(..., description="Client or company to search memories for", examples=["Acme Corporation"])
    query: str = Field(..., description="Semantic search query or topic to recall", examples=["security concerns and deployment preferences"])
    bank_id: Optional[str] = Field(None, description="Optional override for Hindsight bank ID")


class MemoryItem(BaseModel):
    id: Optional[str] = Field(None, description="Memory ID from Hindsight or fallback")
    content: str = Field(..., description="Recalled memory text or fact")
    score: Optional[float] = Field(None, description="Relevance score if returned by Hindsight")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with memory (date, contact, tags)")
    network: Optional[str] = Field(None, description="Hindsight network (world, experience, observation, opinion)")
    timestamp: Optional[str] = Field(None, description="Timestamp of when memory occurred or was retained")
    provider: Literal["hindsight", "local_fallback"] = Field("hindsight", description="Actual provider that supplied this memory item")


class MemoryRecallResponse(BaseModel):
    client: str
    query: str
    total_recalled: int
    memories: List[MemoryItem]
    hindsight_connected: bool
    status_message: str
    memory_provider: Literal["hindsight", "local_fallback"] = Field(..., description="Memory provider used: 'hindsight' or 'local_fallback'")
    memory_info: MemoryOperationInfo = Field(..., description="Detailed memory operation telemetry")
