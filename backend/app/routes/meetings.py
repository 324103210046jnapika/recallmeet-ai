from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..schemas.meeting import MeetingCreate, MeetingResponse, MeetingListResponse
from ..schemas.prepare import MeetingPrepareRequest, MeetingPrepareResponse
from ..services.meeting_service import meeting_service
from ..services.prep_service import prep_service


router = APIRouter(prefix="/api/meetings", tags=["Meetings"])


@router.post(
    "",
    response_model=MeetingResponse,
    status_code=201,
    summary="Create and Retain Meeting"
)
async def create_meeting(meeting: MeetingCreate) -> MeetingResponse:
    """
    Creates a new meeting record, formats it into structured episodic intelligence,
    and retains it directly into Hindsight memory bank with metadata and tags.
    """
    try:
        return await meeting_service.create_meeting(meeting)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to record and retain meeting: {str(e)}"
        )


@router.post(
    "/seed",
    summary="Seed Demo Meetings (Acme & NovaHealth)"
)
async def seed_demo_data():
    """
    Seeds the 4 progressive Acme Corporation meetings and 2 NovaHealth Systems
    meetings directly into Hindsight and the local store.
    """
    from seed_data import DEMO_MEETINGS

    results = []

    for idx, meeting in enumerate(DEMO_MEETINGS, 1):
        saved = await meeting_service.create_meeting(
            meeting,
            custom_id=f"demo_{idx}"
        )
        results.append(saved)

    return {
        "status": "success",
        "message": f"Seeded {len(results)} demo meetings into Hindsight memory",
        "meetings_seeded": len(results)
    }


@router.get(
    "",
    response_model=MeetingListResponse,
    summary="List Meeting History"
)
def list_meetings(
    client: Optional[str] = Query(
        None,
        description="Filter meetings by client or company name"
    )
) -> MeetingListResponse:
    """
    Retrieves chronological meeting history, optionally filtered by client.
    """
    meetings = meeting_service.get_meetings(client=client)

    return MeetingListResponse(
        total=len(meetings),
        client=client,
        meetings=meetings
    )


@router.get(
    "/{meeting_id}",
    response_model=MeetingResponse,
    summary="Get Meeting by ID"
)
def get_meeting(meeting_id: str) -> MeetingResponse:
    """
    Retrieves specific meeting details by ID.
    """
    meeting = meeting_service.get_meeting(meeting_id)

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail=f"Meeting '{meeting_id}' not found."
        )

    return meeting


@router.post(
    "/prepare",
    response_model=MeetingPrepareResponse,
    summary="Generate Executive Meeting Preparation Brief"
)
async def prepare_meeting(
    request: MeetingPrepareRequest
) -> MeetingPrepareResponse:
    """
    Generates an AI meeting preparation briefing using Hindsight persistent memory.

    - When memory_enabled=true:
      Hindsight recalls historical commitments, unresolved concerns,
      and technical constraints to ground the LLM's synthesis.

    - When memory_enabled=false:
      Demonstrates the baseline without Hindsight memory.
    """
    try:
        return await prep_service.prepare_meeting(request)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to synthesize meeting prep: {str(e)}"
        )