from fastapi import APIRouter, HTTPException
from ..schemas.insight import ClientInsightResponse
from ..services.insight_service import insight_service

router = APIRouter(prefix="/api/insights", tags=["Insights"])


@router.get("/{client}", response_model=ClientInsightResponse, summary="Get Client Insights & Evolution")
def get_client_insights(client: str) -> ClientInsightResponse:
    """
    Returns strategic client intelligence:
    - Number of interactions
    - Open commitments
    - Recurring concerns
    - Known technical preferences
    - Recent changes
    - Unresolved topics
    """
    try:
        return insight_service.get_client_insights(client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")
