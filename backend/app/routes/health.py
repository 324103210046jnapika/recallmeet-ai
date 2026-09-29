from fastapi import APIRouter
from typing import Dict, Any

from ..config import settings
from ..services.hindsight_service import hindsight_service
from ..services.llm_service import llm_service
from ..services.meeting_service import meeting_service


router = APIRouter(
    prefix="/api",
    tags=["Health & Diagnostics"]
)


@router.get(
    "/health",
    summary="System Health & Hindsight Diagnostics"
)
async def health_check() -> Dict[str, Any]:
    """
    Returns system health and comprehensive Hindsight diagnostics:

    - Hindsight configured
    - Hindsight reachable
    - Hindsight bank
    - Hindsight version
    - Last operation status
    - LLM status
    - Meeting statistics
    """

    # Hindsight SDK operations are asynchronous.
    hindsight_info = await hindsight_service.check_connection()

    # LLM health check remains synchronous.
    llm_info = llm_service.check_health()

    # Local meeting store remains synchronous.
    all_meetings = meeting_service.get_meetings()

    is_connected = hindsight_info.get("connected", False)

    is_configured = hindsight_info.get(
        "configured",
        bool(settings.HINDSIGHT_BASE_URL)
    )

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,

        # Direct Hindsight diagnostics
        "hindsight_configured": is_configured,
        "hindsight_reachable": is_connected,
        "hindsight_bank": settings.HINDSIGHT_BANK_ID,
        "hindsight_version": hindsight_info.get("version"),

        "last_operation_status": (
            hindsight_service.last_operation_status
        ),

        # Detailed Hindsight information
        "hindsight": {
            "configured": is_configured,
            "connected": is_connected,
            "configured_base_url": settings.HINDSIGHT_BASE_URL,
            "bank_id": settings.HINDSIGHT_BANK_ID,
            "version": hindsight_info.get("version"),
            "has_api_key": bool(settings.HINDSIGHT_API_KEY),
            "error": hindsight_info.get("error"),

            "last_operation": (
                hindsight_service.last_operation_status
            )
        },

        # LLM diagnostics
        "llm": {
            "provider": "Groq",
            "model": settings.GROQ_MODEL,
            "status": llm_info.get("status")
        },

        # Application statistics
        "stats": {
            "total_meetings_recorded": len(all_meetings),
            "unique_clients": len(
                meeting_service.get_clients()
            )
        }
    }