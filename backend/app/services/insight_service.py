from typing import List, Dict, Any
from ..schemas.insight import ClientInsightResponse
from ..services.meeting_service import meeting_service
from ..services.hindsight_service import hindsight_service
from ..utils.logger import logger


class InsightService:
    def get_client_insights(self, client: str) -> ClientInsightResponse:
        """Derive actionable client insights from meeting history and Hindsight memory."""
        meetings = meeting_service.get_meetings(client=client)
        if not meetings:
            return ClientInsightResponse(
                client=client,
                number_of_interactions=0,
                open_commitments=[],
                recurring_concerns=[],
                known_preferences=[],
                recent_changes=[],
                unresolved_topics=[]
            )

        # Aggregate across historical meetings
        commitments: List[str] = []
        concerns: List[str] = []
        decisions: List[str] = []
        follow_ups: List[str] = []

        for m in meetings:
            commitments.extend(m.commitments or [])
            concerns.extend(m.concerns or [])
            decisions.extend(m.decisions or [])
            follow_ups.extend(m.follow_ups or [])

        # Deduplicate while preserving order
        unique_commitments = list(dict.fromkeys(commitments))
        unique_concerns = list(dict.fromkeys(concerns))
        unique_preferences = list(dict.fromkeys(decisions))

        # Detect recent changes chronologically
        recent_changes: List[str] = []
        if len(meetings) >= 2:
            for i in range(1, len(meetings)):
                prev = meetings[i - 1]
                curr = meetings[i]
                recent_changes.append(
                    f"Progressed from '{prev.title}' ({prev.date}) to '{curr.title}' ({curr.date})"
                )
        elif len(meetings) == 1:
            recent_changes.append(f"Initial discovery established on {meetings[0].date}")

        # Unresolved topics: concerns or follow_ups not explicitly marked resolved
        unresolved_topics: List[str] = []
        for c in unique_concerns:
            if any(kw in c.lower() for kw in ["unresolved", "pending", "concern", "worry", "risk", "must", "required"]):
                unresolved_topics.append(c)
        for f in follow_ups:
            if "deliver" in f.lower() or "review" in f.lower() or "schedule" in f.lower() or "provide" in f.lower():
                unresolved_topics.append(f)

        unresolved_topics = list(dict.fromkeys(unresolved_topics))

        return ClientInsightResponse(
            client=client,
            number_of_interactions=len(meetings),
            open_commitments=unique_commitments,
            recurring_concerns=unique_concerns,
            known_preferences=unique_preferences,
            recent_changes=recent_changes,
            unresolved_topics=unresolved_topics
        )


insight_service = InsightService()
