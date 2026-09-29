from typing import List
from pydantic import BaseModel, Field


class ClientInsightResponse(BaseModel):
    client: str = Field(..., description="Client name")
    number_of_interactions: int = Field(0, description="Total interactions/meetings recorded")
    open_commitments: List[str] = Field(default_factory=list, description="All promises or commitments made to the client")
    recurring_concerns: List[str] = Field(default_factory=list, description="Repeated or unresolved objections and concerns")
    known_preferences: List[str] = Field(default_factory=list, description="Client technical preferences, constraints, or decisions")
    recent_changes: List[str] = Field(default_factory=list, description="Evolution or changes detected across meeting history")
    unresolved_topics: List[str] = Field(default_factory=list, description="Pending reviews or questions needing resolution")
