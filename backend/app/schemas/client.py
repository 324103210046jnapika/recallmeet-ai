from typing import List, Optional
from pydantic import BaseModel, Field


class ClientSummary(BaseModel):
    name: str = Field(..., description="Client name")
    primary_contact: Optional[str] = Field(None, description="Primary contact name and title")
    total_meetings: int = Field(0, description="Total recorded meetings")
    last_interaction: Optional[str] = Field(None, description="Date of last recorded meeting")


class ClientDetail(ClientSummary):
    first_interaction: Optional[str] = None
    known_priorities: List[str] = Field(default_factory=list)
    contacts: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
